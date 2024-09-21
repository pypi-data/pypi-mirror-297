import os
import argparse
import cv2
import numpy as np
import csv
import logging
import glob
from abc import ABC, ABCMeta, abstractmethod
from pathlib import Path
import ast
from typing import Union, Dict, List, Tuple
from sklearn.metrics import confusion_matrix

class EvaluationKey(metaclass=ABCMeta):
    """
    Abstract base class representing keys used for evaluation.
    """
    @abstractmethod
    def __hash__(self) -> int:
        """Abstract method for hashing."""
        raise NotImplementedError()

    @abstractmethod
    def __eq__(self, other) -> bool:
        """Abstract method for equality."""
        raise NotImplementedError()

    @abstractmethod
    def __repr__(self) -> str:
        """Abstract method for representation."""
        raise NotImplementedError()

class ImageKey(EvaluationKey):
    """
    Subclass of EvaluationKey representing keys for image file paths.
    """
    def __init__(self, image_fpath: Union[str, Path], base_dpath: Union[str, Path]) -> None:
        """
        Initialize ImageKey with an image file path.

        Args:
            image_fpath (Union[str, Path]): Full Path to the image file.
            base_dpath (Union[str, Path]): Base path of the image.
            _rel_fpath (Path): Relative file path of the image.
        """
        self._image_fpath = Path(image_fpath)
        self._base_dpath = Path(base_dpath)
        self._rel_fpath = self._image_fpath.relative_to(self._base_dpath)

    def __hash__(self) -> int:
        """
        Hash method based on the relative file path of the image.

        Returns:
            int: Hash value.
        """
        return hash(str(self._rel_fpath))

    def __eq__(self, other) -> bool:
        """
        Equality method based on the relative file path of the image.

        Returns:
            bool: True if the other object is an ImageKey with the same relative file path, False otherwise.
        """
        return isinstance(other, ImageKey) and self._rel_fpath == other._rel_fpath

    def __repr__(self) -> str:
        """
        Representation of the ImageKey.

        Returns:
            str: Representation of the relative path in ImageKey.
        """
        return f"{self._rel_fpath}"

class EvaluationInstance:
    """
    Abstract base class representing instances used for evaluation.
    """
    @abstractmethod
    def load(self) -> None:
        """Abstract method for loading data."""
        raise NotImplementedError()

class ImageInstance(EvaluationInstance):
    """
    Subclass of EvaluationInstance representing instances of image data.
    """
    def __init__(self, eval_key: ImageKey, basepath: Union[str, Path]) -> None:
        """
        Initialize ImageInstance with an image file path.

        Args:
            eval_key: Eval(ImageKey) instance.
            basepath: Base path of the image directory.
            image_fpath: Full absolute path of the image.
        """
        self._basepath = Path(basepath)
        self._image_fpath = self._basepath.joinpath(repr(eval_key))

    def load(self) -> np.ndarray:
        """
        Load image data using OpenCV.

        Returns:
            np.ndarray: Loaded image data.
        """
        if self._image_fpath.exists():
            # Load the image using OpenCV in BGR format.
            image = cv2.imread(str(self._image_fpath), cv2.IMREAD_COLOR)
        return image

class SemanticSegmentationMatchCalculator:
    """
    Class for calculating matches between query and reference instances.
    """
    def __init__(self, to_ignore: bool, ignore_pixels: list, quotient_mapping: Dict[Tuple[int, int, int], Tuple[int, int, int]] = None) -> None:
        """
        Initialize SemanticSegmentationMatchCalculator.

        Args:
            to_ignore: Boolean value to check if certain pixels are to be ignored.
            ignore_pixels: List of pixel values to be ignored.
            quotient_mapping (Dict[Tuple[int, int, int], Tuple[int, int, int]], optional): Mapping of original colors to quotient colors. Defaults to None.
        """
        self._to_ignore = to_ignore
        self._ignore_pixels = ignore_pixels
        self._quotient_mapping = quotient_mapping

    def apply_quotient_mapping(self, image: np.ndarray) -> np.ndarray:
        """
        Apply the quotient mapping to an input image.

        This method creates a new image where each pixel color is replaced with its corresponding
        quotient color if it exists in the quotient mapping. Unmapped colors remain unchanged.

        Args:
            image (np.ndarray): Input image to apply quotient mapping to.

        Returns:
            np.ndarray: New image with quotient mapping applied.
        """
        output = np.copy(image)  # Create a copy of the input image
        mapped_mask = np.zeros(image.shape[:2], dtype=bool)  # Track mapped pixels
        
        for original, mapped in self._quotient_mapping.items():
            mask = np.all(image == original, axis=-1)
            output[mask] = mapped
            mapped_mask |= mask  # Update mapped mask
        
        # Set only unmapped pixels to the ignore value
        output[~mapped_mask] = self._to_ignore
        
        return output

    def create_annulus_mask(self, h, w, center, min_radius, max_radius):
        """
        Create an annulus mask.

        Args:
            h, w: Height and width of the mask
            center: Center of the annulus
            min_radius: Inner radius of the annulus
            max_radius: Outer radius of the annulus

        Returns:
            mask: Boolean mask with True values inside the annulus
        """
        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)
        mask = (dist_from_center >= min_radius) & (dist_from_center <= max_radius)
        return mask

    def match(self, query: ImageInstance, reference: ImageInstance, min_radius: float, max_radius: float) -> dict:
        """
        Compute matching pixels and unmatched counts for semantic segmentation evaluation.

        Args:
            query: Query instance (Query ImageInstance).
            reference: Reference instance (Reference Instance).
            min_radius: Inner radius for masking (in cells)
            max_radius: Outer radius for masking (in cells)

        Returns:
            matches: Dictionary containing match information for each class and overall values for every class.
            confusion_matrix_map: Dictionary containing confusion matrix for each class.
        """
        # Load query and reference images.
        query_image = query.load()
        reference_image = reference.load()

        # Check if the query and reference images have the same size
        if query_image.shape != reference_image.shape:
            raise ValueError(f"Query and reference images must have the same size. Query size: {query_image.shape}, Reference size: {reference_image.shape}")

        # Check if the query and reference images have the same type
        if query_image.dtype != reference_image.dtype:
            raise ValueError(f"Query and reference images must have the same type. Query dtype: {query_image.dtype}, Reference dtype: {reference_image.dtype}")

        if self._quotient_mapping is not None:
            query_image = self.apply_quotient_mapping(query_image)
            reference_image = self.apply_quotient_mapping(reference_image)

        # Check if both radii are infinity (regular evaluation)
        if min_radius == float('inf') and max_radius == float('inf'):
            mask = np.ones(query_image.shape[:2], dtype=bool)
        else:
            # Create annulus mask
            h, w = query_image.shape[:2]
            center = (w // 2, h // 2)
            mask = self.create_annulus_mask(h, w, center, min_radius, max_radius)

        # Apply mask to both query and reference images
        query_image_masked = query_image.copy()
        reference_image_masked = reference_image.copy()
        query_image_masked[~mask] = self._ignore_pixels
        reference_image_masked[~mask] = self._ignore_pixels

        # Create a 2D array of pixels for query and reference images. 
        query_pixels = np.reshape(query_image_masked, (-1, 3))
        reference_pixels = np.reshape(reference_image_masked, (-1, 3))

        # Check if certain pixels are to be ignored
        if self._to_ignore:
            # Find the indices of pixels to be ignored in the query and reference image.
            reference_ignore_indices = np.where(np.all(reference_pixels == self._ignore_pixels, axis=1))[0]
            query_ignore_indices = np.where(np.all(query_pixels == self._ignore_pixels, axis=1))[0]

            # Find the union of indices to be ignored.
            ignore_indices = np.union1d(reference_ignore_indices, query_ignore_indices)

            # Filter to the pixels in the reference image to those whose pixel index is not in ignore_indices.
            reference_pixels = np.delete(reference_pixels, ignore_indices, axis=0)

            # Filter to the pixels in the query image to those whose pixel index is not in ignore_indices.
            query_pixels = np.delete(query_pixels, ignore_indices, axis=0)

        # Get unique classes from the query image and the reference image.
        unique_classes_query = set(map(tuple, query_pixels))
        unique_classes_reference = set(map(tuple, reference_pixels))

        # Get the unique classes present in both the query and reference images.
        unique_classes = unique_classes_query.union(unique_classes_reference)

        # Create dictionaries to map RGB tuples to indices
        class_to_index = {cls: idx for idx, cls in enumerate(unique_classes)}
        # Convert RGB tuples to indices for both reference and query pixels
        reference_labels = [class_to_index[tuple(rgb)] for rgb in reference_pixels]
        query_labels = [class_to_index[tuple(rgb)] for rgb in query_pixels]
        # Compute confusion matrix using the reference and query labels
        confusion_mat = confusion_matrix(reference_labels, query_labels, labels=list(class_to_index.values()))

        # Convert the confusion matrix into a map for each query and reference image.
        confusion_matrix_map = {ref_cls: {query_cls: int(confusion_mat[i, j]) 
                                for j, query_cls in enumerate(unique_classes_query)}
                                for i, ref_cls in enumerate(unique_classes_reference)}

        # Initialize dictionary to store match information for each class and overall values.      
        matches = {}
        #Iterate over each class and calculate the number of matched pixels, unmatched query pixels, and unmatched reference pixels.
        for cls in unique_classes:
            # Get the pixels of the class from the query and reference images.
            query_class_pixels = np.where(np.all(query_pixels == np.array(cls), axis = 1))[0]
            reference_class_pixels = np.where(np.all(reference_pixels == np.array(cls), axis = 1))[0]

            # Calculate the number of matched pixels, unmatched query pixels, and unmatched reference pixels.
            matched_pixels = np.intersect1d(query_class_pixels, reference_class_pixels).shape[0]
            unmatched_query_pixels = np.setdiff1d(query_class_pixels, reference_class_pixels).shape[0]
            unmatched_reference_pixels = np.setdiff1d(reference_class_pixels, query_class_pixels).shape[0]

            # Store the match information for the class.
            matches[cls] = {
                'num_matches': matched_pixels, 
                'num_unmatched_queries': unmatched_query_pixels, 
                'num_unmatched_references': unmatched_reference_pixels, 
                'num_query_pixels': query_class_pixels.shape[0], 
                'num_reference_pixels': reference_class_pixels.shape[0]
            }
        
        # Calculate overall values for all the classes.
        matches['overall'] = {
            'num_matches': sum([matches[cls]['num_matches'] for cls in matches]),       
            'num_unmatched_queries': sum([matches[cls]['num_unmatched_queries'] for cls in matches]), 
            'num_unmatched_references': sum([matches[cls]['num_unmatched_references'] for cls in matches]),
            'num_query_pixels': sum([matches[cls]['num_query_pixels'] for cls in matches]),
            'num_reference_pixels': sum([matches[cls]['num_reference_pixels'] for cls in matches])
        }

        matches['query_image_fpath'] = str(query._image_fpath)
        matches['reference_image_fpath'] = str(reference._image_fpath)
        matches['min_radius'] = min_radius
        matches['max_radius'] = max_radius

        confusion_matrix_map['query_image_fpath'] = str(query._image_fpath)
        confusion_matrix_map['reference_image_fpath'] = str(reference._image_fpath)
        confusion_matrix_map['min_radius'] = min_radius
        confusion_matrix_map['max_radius'] = max_radius

        return matches, confusion_matrix_map

class MetricsSummarizer(ABC):
    """
    Abstract superclass for summarizing evaluation metrics.
    """
    @abstractmethod
    def summarize(self, matches: dict, output_filename: str) -> dict:
        """
        Summarize evaluation metrics.

        Args:
            matches: matches match data in the form of dict.
            output_filename: Name of the output file to write the metrics.
        """
        raise NotImplementedError()

class SummarizeMetrics(MetricsSummarizer):
    """
    Subclass of MetricsSummarizer for summarizing evaluation metrics.
    """
    def __init__(self) -> None:
        """
        Initialize SummarizeMetrics.

        Args:
            _metrics: Dictionary containing calculated metrics for each classes and overall calculations as well.
            {
                class 1: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                class 2: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},

                class n: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                overall: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
            }
            _per_image_metrics: Dictionary containing calculated metrics for each image.
            {
                image_name1: {
                    class 1: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                    class 2: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},

                    'overall': { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
                    'query_image_fpath': 'str',
                    'reference_image_fpath': 'str'
                    'radius': float
                },
                image_name2: {

                },

            }
        """
        self._metrics = {}
        self._per_image_metrics = {}
        self._confusion_matrix = {}
        self._per_image_confusion_matrix = {}
    
    def calculate_overall_metrics(self, matches: dict) -> dict:
        """
        Calculate precision, recall, and iou metrics.

        Args:
            matches: matches match data in the form of dict.
            {
                class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},

                class n: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                overall: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
            }
        
        Returns:
            metrics: Dictionary containing calculated metrics for each class and overall calculations as well.
            {
                class 1: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                class 2: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},

                class n: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                overall: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
            }
        """
        metrics = {}
        for (min_radius, max_radius), radius_data in matches.items():
            metrics[(min_radius, max_radius)] = {}
            total_matches = 0
            total_unmatched_queries = 0
            total_unmatched_references = 0
            total_query_pixels = 0
            total_reference_pixels = 0
            
            for key, values in radius_data.items():
                if isinstance(values, dict) and 'num_matches' in values:
                    if key != 'overall':  # Skip the 'overall' key to avoid double-counting
                        num_matches = values['num_matches']
                        num_unmatched_queries = values['num_unmatched_queries']
                        num_unmatched_references = values['num_unmatched_references']
                        num_query_pixels = values['num_query_pixels']
                        num_reference_pixels = values['num_reference_pixels']
                        
                        total_matches += num_matches
                        total_unmatched_queries += num_unmatched_queries
                        total_unmatched_references += num_unmatched_references
                        total_query_pixels += num_query_pixels
                        total_reference_pixels += num_reference_pixels
                        
                        if num_matches == 0:
                            metrics[(min_radius, max_radius)][key] = {
                                'precision': 0.0, 
                                'recall': 0.0, 
                                'iou': 0.0, 
                                'num_matches': 0, 
                                'num_unmatched_queries': num_unmatched_queries, 
                                'num_unmatched_references': num_unmatched_references,
                                'num_query_pixels': num_query_pixels, 
                                'num_reference_pixels': num_reference_pixels
                            }
                        else:
                            precision = num_matches / (num_matches + num_unmatched_queries)
                            recall = num_matches / (num_matches + num_unmatched_references)
                            iou = num_matches / (num_matches + num_unmatched_queries + num_unmatched_references)
                            metrics[(min_radius, max_radius)][key] = {
                                'precision': precision, 
                                'recall': recall, 
                                'iou': iou, 
                                'num_matches': num_matches, 
                                'num_unmatched_queries': num_unmatched_queries, 
                                'num_unmatched_references': num_unmatched_references,
                                'num_query_pixels': num_query_pixels, 
                                'num_reference_pixels': num_reference_pixels
                            }
            
            # Calculate overall metrics
            overall_precision = total_matches / (total_matches + total_unmatched_queries) if (total_matches + total_unmatched_queries) > 0 else 0
            overall_recall = total_matches / (total_matches + total_unmatched_references) if (total_matches + total_unmatched_references) > 0 else 0
            overall_iou = total_matches / (total_matches + total_unmatched_queries + total_unmatched_references) if (total_matches + total_unmatched_queries + total_unmatched_references) > 0 else 0
            
            metrics[(min_radius, max_radius)]['overall'] = {
                'precision': overall_precision,
                'recall': overall_recall,
                'iou': overall_iou,
                'num_matches': total_matches,
                'num_unmatched_queries': total_unmatched_queries,
                'num_unmatched_references': total_unmatched_references,
                'num_query_pixels': total_query_pixels,
                'num_reference_pixels': total_reference_pixels
            }
        
        return metrics

    def calculate_per_image_metrics(self, per_image_matches: dict) -> dict:
        """
        Calculate precision, recall, and iou metrics for each class and overall for each image.

        Args:
            per_image_matches: Dictionary containing match information for every image and classes present in it.
            {
                image_name1: {
                    class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int , 'num_query_pixels': int, 'num_reference_pixels': int},
                    class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                    
                    'overall': { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
                    'query_image_fpath': 'str',
                    'reference_image_fpath': 'str'
                    'radius': float
                },
                image_name2: {
                    class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                    class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},

                    'overall': { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
                    'query_image_fpath': 'str',
                    'reference_image_fpath': 'str'
                    'radius': float
                },

            }

        Returns:
            per_image_metrics: Dictionary containing calculated metrics for each image.
            {
                image_name1: {
                    class 1: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                    class 2: { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},

                    'overall': { 'precision': float, 'recall': float, 'iou': float, 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
                    'query_image_fpath': 'str',
                    'reference_image_fpath': 'str'
                    'radius': float
                },
                image_name2: {

                },

            }
        """
        per_image_metrics = {}
        for image_key, image_data in per_image_matches.items():
            image_metrics = {}
            for key, values in image_data.items():
                if isinstance(values, dict) and 'num_matches' in values:
                    num_matches = values['num_matches']
                    num_unmatched_queries = values['num_unmatched_queries']
                    num_unmatched_references = values['num_unmatched_references']
                    num_query_pixels = values['num_query_pixels']
                    num_reference_pixels = values['num_reference_pixels']
                    if num_matches == 0:
                        image_metrics[key] = {
                            'precision': 0.0, 
                            'recall': 0.0, 
                            'iou': 0.0, 
                            'num_matches': 0, 
                            'num_unmatched_queries': num_unmatched_queries, 
                            'num_unmatched_references': num_unmatched_references,
                            'num_query_pixels': num_query_pixels, 
                            'num_reference_pixels': num_reference_pixels
                        }
                    else:
                        precision = num_matches / (num_matches + num_unmatched_queries)
                        recall = num_matches / (num_matches + num_unmatched_references)
                        iou = num_matches / (num_matches + num_unmatched_queries + num_unmatched_references)
                        image_metrics[key] = {
                            'precision': precision, 
                            'recall': recall, 
                            'iou': iou, 
                            'num_matches': num_matches, 
                            'num_unmatched_queries': num_unmatched_queries, 
                            'num_unmatched_references': num_unmatched_references,
                            'num_query_pixels': num_query_pixels, 
                            'num_reference_pixels': num_reference_pixels
                        }
            image_metrics['query_image_fpath'] = image_data['query_image_fpath']
            image_metrics['reference_image_fpath'] = image_data['reference_image_fpath']
            image_metrics['min_radius'] = image_data['min_radius']
            image_metrics['max_radius'] = image_data['max_radius']
            per_image_metrics[image_key] = image_metrics
        return per_image_metrics
    
    def write_overall_confusion_matrix_to_csv(self, output_file: str) -> None:
        """
        Write confusion matrix to a CSV file.

        confusion_matrix: Dictionary containing confusion matrix for each class.
        {
            reference_class 1: {query_class 1 : np.int64, query_class 2 : np.int64, query_class 3 : np.int64, ...},
            reference_class 2: {query_class 1 : np.int64, query_class 2 : np.int64, query_class 3 : np.int64, ...},
            reference_class 3: {query_class 1 : np.int64, query_class 2 : np.int64, query_class 3 : np.int64, ...},
            reference_class n: {query_class 1 : np.int64, query_class 2 : np.int64, query_class 3 : np.int64, ...}
        }

        Args:
            output_file: Name of the output file.
        """
        # Write confusion matrix to a CSV file
        with open(output_file + '_confusion_matrix.csv', 'w', newline='') as csvfile:
            # Get all unique classes across the confusion matrix
            fieldnames = ['Reference/Query']
            for values in self._confusion_matrix.values():
                if isinstance(values, dict):
                    fieldnames.extend(values.keys())
            fieldnames = list(dict.fromkeys(fieldnames))  # remove duplicates

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key, values in self._confusion_matrix.items():
                if isinstance(values, dict):
                    values = {'Reference/Query': key, **values}
                    writer.writerow(values)

    def write_overall_metrics_to_csv(self, output_file: str)  -> None:
        """
        Write evaluation metrics to a CSV file.

        Args:
            output_file: Name of the output file.
        """ 
        with open(output_file + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['min_radius', 'max_radius', 'class', 'precision', 'recall', 'iou', 'num_matches', 'num_unmatched_queries', 'num_unmatched_references', 'num_query_pixels', 'num_reference_pixels']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for (min_radius, max_radius), radius_data in self._metrics.items():
                for key, values in radius_data.items():
                    if isinstance(values, dict):
                        writer.writerow({
                            'min_radius': min_radius,
                            'max_radius': max_radius,
                            'class': key, 
                            'precision': values['precision'], 
                            'recall': values['recall'], 
                            'iou': values['iou'], 
                            'num_matches': values['num_matches'], 
                            'num_unmatched_queries': values['num_unmatched_queries'], 
                            'num_unmatched_references': values['num_unmatched_references'], 
                            'num_query_pixels': values['num_query_pixels'], 
                            'num_reference_pixels': values['num_reference_pixels']
                        })

    def write_per_image_metrics_to_csv(self, output_file: str) -> None:
        """
        Write per-image evaluation metrics to a CSV file.

        Args:
            output_file: Name of the output file.
        """
        # Write per class metrics to a CSV file per image
        with open(output_file + '_per_image_per_color.csv', 'w', newline='') as csvfile:
            fieldnames = ['image_name', 'min_radius', 'max_radius', 'class', 'precision', 'recall', 'iou', 'num_matches', 'num_unmatched_queries', 'num_unmatched_references', 'num_query_pixels', 'num_reference_pixels', 'query_image_fpath', 'reference_image_fpath']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for key, values in self._per_image_metrics.items():
                for k, v in values.items():
                    if isinstance(v, dict) and 'precision' in v:
                        writer.writerow({
                            'image_name': key, 
                            'min_radius': values['min_radius'],
                            'max_radius': values['max_radius'],
                            'class': k, 
                            'precision': v['precision'], 
                            'recall': v['recall'], 
                            'iou': v['iou'], 
                            'num_matches': v['num_matches'], 
                            'num_unmatched_queries': v['num_unmatched_queries'], 
                            'num_unmatched_references': v['num_unmatched_references'], 
                            'num_query_pixels': v['num_query_pixels'], 
                            'num_reference_pixels': v['num_reference_pixels'],
                            'query_image_fpath': values['query_image_fpath'], 
                            'reference_image_fpath': values['reference_image_fpath']
                        })                

        # Write overall metrics to a CSV file per image
        with open(output_file + '_per_image.csv', 'w', newline='') as csvfile:
            fieldnames = ['image_name', 'min_radius', 'max_radius', 'precision', 'recall', 'iou', 'num_matches', 'num_unmatched_queries', 'num_unmatched_references', 'num_query_pixels', 'num_reference_pixels', 'query_image_fpath', 'reference_image_fpath']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for key, values in self._per_image_metrics.items():
                if isinstance(values, dict) and 'overall' in values:
                    writer.writerow({
                        'image_name': key, 
                        'min_radius': values['min_radius'],
                        'max_radius': values['max_radius'],
                        'precision': values['overall']['precision'], 
                        'recall': values['overall']['recall'], 
                        'iou': values['overall']['iou'], 
                        'num_matches': values['overall']['num_matches'], 
                        'num_unmatched_queries': values['overall']['num_unmatched_queries'], 
                        'num_unmatched_references': values['overall']['num_unmatched_references'], 
                        'num_query_pixels': values['overall']['num_query_pixels'], 
                        'num_reference_pixels': values['overall']['num_reference_pixels'],
                        'query_image_fpath': values['query_image_fpath'], 
                        'reference_image_fpath': values['reference_image_fpath']
                    })

    def write_per_image_confusion_matrix_to_csv(self, output_file: str) -> None:
        """
        Write confusion matrix to a CSV file.

        per_image_confusion_matrix: Dictionary containing confusion matrix for each class for each image.
        """
        # Get all unique query classes across the confusion matrix
        all_query_classes = set()
        for image_data in self._per_image_confusion_matrix.values():
            for ref_class, query_classes in image_data.items():
                if isinstance(query_classes, dict):
                    all_query_classes.update(query_classes.keys())

        # Write confusion matrix to a CSV file
        with open(output_file + '_per_image_confusion_matrix.csv', 'w', newline='') as csvfile:
            # Define the fieldnames
            fieldnames = ['Image Name', 'Reference/Query'] + list(all_query_classes) + ['Query Image Path', 'Reference Image Path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for image_name, image_data in self._per_image_confusion_matrix.items():
                for ref_class, query_classes in image_data.items():
                    if isinstance(query_classes, dict):
                        row = {
                            'Image Name': image_name, 
                            'Reference/Query': ref_class,
                            'Query Image Path': image_data['query_image_fpath'], 
                            'Reference Image Path': image_data['reference_image_fpath']
                        }
                        row.update(query_classes)
                        writer.writerow(row)

    def print_metrics(self) -> None:
        """
        Print evaluation metrics.
        """
        print("\nMetrics: ")
        for radius, radius_data in self._metrics.items():
            print(f"\nRadius: {radius}")
            for key, values in radius_data.items():
                print(f"{key}: precision = {values['precision']}, recall = {values['recall']}, iou = {values['iou']}, num_matches = {values['num_matches']}, num_unmatched_queries = {values['num_unmatched_queries']}, num_unmatched_references = {values['num_unmatched_references']}, num_query_pixels = {values['num_query_pixels']}, num_reference_pixels = {values['num_reference_pixels']}")

    def summarize(self, matches: dict, per_image_matches: dict, confusion_matrix: dict, per_image_confusion_matrix: dict, output_filename: str) -> dict:
        """
        Summarize evaluation metrics.

        Args:
            matches: matches match data in the form of dict.
            {
                class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},

                class n: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                overall: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
            }

            per_image_matches: Dictionary containing match information for every images and classes present in it.
            {
                image_name1: {
                    class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                    class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                    
                    'overall': { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
                },
                image_name2: {

                },
            }

            output_filename: Name of the output file to write the metrics.
        """
        self._metrics = self.calculate_overall_metrics(matches)
        self._per_image_metrics = self.calculate_per_image_metrics(per_image_matches)
        self._confusion_matrix = confusion_matrix
        self._per_image_confusion_matrix = per_image_confusion_matrix
        self.write_overall_metrics_to_csv(output_filename)
        self.write_per_image_metrics_to_csv(output_filename)
        self.write_overall_confusion_matrix_to_csv(output_filename)
        self.write_per_image_confusion_matrix_to_csv(output_filename)
        self.print_metrics()

def dict_matches_adder(matches: dict, current: dict) -> dict:
    """
    Take the current dictionary values and add them to the matches dictionary.

    Args:
        matches: matches dictionary. It is accumulation of all the values from all the iterated ImageInstance so far.
        {
            class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
            class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int , 'num_query_pixels': int, 'num_reference_pixels': int},
            
            class n: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int , 'num_query_pixels': int, 'num_reference_pixels': int},
            overall: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int , 'num_query_pixels': int, 'num_reference_pixels': int}
            'query_image_fpath': str,
            'reference_image_fpath': str
            'radius': float
        }
        current: Current dictionary to add. It is the match data from a current single ImageInstance.
        {
            class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int , 'num_query_pixels': int, 'num_reference_pixels': int},
            class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int , 'num_query_pixels': int, 'num_reference_pixels': int},
            
            class n: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
            overall: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int,  'num_query_pixels': int, 'num_reference_pixels': int}
            'query_image_fpath': str,
            'reference_image_fpath': str
            'radius': float
        }

    Returns:
        matches: Updated matches dictionary. It add the current dictionary values to the matches dictionary. and returns the updated matches dictionary.
        {
            class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
            class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
            
            class n: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
            overall: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
        }
    """
    min_radius = current.get('min_radius', float('inf'))
    max_radius = current.get('max_radius', float('inf'))
    key = (min_radius, max_radius)
    
    if key not in matches:
        matches[key] = {}

    for k, value in current.items():
        if k in ['min_radius', 'max_radius']:
            continue
        if k not in matches[key]:
            if isinstance(value, dict):
                matches[key][k] = value.copy()
            else:
                matches[key][k] = value
        else:
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if subkey in matches[key][k]:
                        matches[key][k][subkey] += subvalue
                    else:
                        matches[key][k][subkey] = subvalue
            elif isinstance(value, (int, float)):
                matches[key][k] += value
    return matches

def dict_matches_appender(per_image_matches: dict, current: dict, key: str) -> dict:
    """
    Take the current dictionary values and append them to the per_image_results dictionary.

    Args:
        per_image_matches: Append per_image_matches dictionary. It is accumulation of all the values from all the iterated ImageInstance so far.
        {
            'image_name1': {
                class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                
                'overall': { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
                'query_image_fpath': str,
                'reference_image_fpath': str
                'radius': float
            },
            'image_name2': {
                class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},

                'overall': { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
                'query_image_fpath': str,
                'reference_image_fpath': str
                'radius': float
            },
        }
        current: Current dictionary to add. It is the match data from a current single ImageInstance.
        {
            class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
            class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
            
            class n: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
            overall: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
            'query_image_fpath': str,
            'reference_image_fpath': str
            'radius': float
        }
        
    Returns:
        per_image_matches: Updated per_image_matches dictionary. It add the current dictionary values to the per_image_matches dictionary. and returns the updated per_image_matches dictionary.
        {
            'image_name1': {
                class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                
                'overall': { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
                'query_image_fpath': str,
                'reference_image_fpath': str
                'radius': float
            },
            'image_name2': {
                class 1: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},
                class 2: { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int},

                'overall': { 'num_matches': int, 'num_unmatched_queries': int, 'num_unmatched_references': int, 'num_query_pixels': int, 'num_reference_pixels': int}
                'query_image_fpath': str,
                'reference_image_fpath': str
                'radius': float
            },
        }
    """
    per_image_matches[str(key)] = current
    return per_image_matches

def parse_args() -> tuple:
    """
    Parse command line arguments.

    Returns:
        tuple: Tuple containing parsed arguments and variables.
    """
    parser = argparse.ArgumentParser(description="Evaluation script")
    parser.add_argument("-q", "--query_image_dir", help="Path to the first directory containing PNG images")
    parser.add_argument("-r", "--reference_image_dir", help="Path to the second directory containing PNG images")
    parser.add_argument("-o", "--output_filename", help="Path to the output file for metrics", default="metrics")
    parser.add_argument("-i", "--to_ignore", help="Permission to ignore pixels or not", default=False, action="store_true")
    parser.add_argument("--quotient-map-fpath", help="Path to JSON file containing quotient class mapping", type=str, default=None)
    parser.add_argument("--min_radius", type=float, help="Minimum radius for evaluation", default=float('inf'))
    parser.add_argument("--max_radius", type=float, help="Maximum radius for evaluation", default=float('inf'))
    parser.add_argument("--step_size", type=float, help="Step size for radius linspace", default=float('inf'))
    args = parser.parse_args()
    var = vars(args)

    # Check for invalid combinations
    if var['min_radius'] != float('inf') and var['step_size'] != float('inf') and var['max_radius'] == float('inf'):
        raise ValueError("Cannot create a finite linspace with infinite max radius when min radius and step size are finite")

    return args, var