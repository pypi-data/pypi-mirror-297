from performance_evaluation_tool import *
import time
import copy
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_quotient_map(file_path: str) -> Dict[Tuple[int, int, int], Tuple[int, int, int]]:
    absolute_path = Path(file_path).resolve()
    with open(absolute_path, 'r') as f:
        quotient_map_str = json.load(f)
    # Use eval to convert string tuples to actual tuples
    quotient_map = {
        eval(k): eval(v)
        for k, v in quotient_map_str.items()
    }
    return quotient_map

def main():
    start_time = time.time()

    # Parse command line arguments
    args, var = parse_args()

    # Check if query and reference image directories are provided
    if var['query_image_dir'] is None or var['reference_image_dir'] is None:
        logging.error("Either Query image directory or Reference image directory is not provided")
        return

    # Retrieve file paths for query and reference images
    query_image_base_dpath = var['query_image_dir']
    reference_image_base_dpath = var['reference_image_dir']
    output_filename = var['output_filename']

    # Create ImageKeys for query and reference images
    query_keys = set(
        [ImageKey(query_image_fpath, query_image_base_dpath)
        for query_image_fpath in glob.glob(f'{query_image_base_dpath}/*.png')])

    reference_keys = set(
        [ImageKey(reference_image_fpath, reference_image_base_dpath)
        for reference_image_fpath in glob.glob(f'{reference_image_base_dpath}/*.png')])

    logging.info(f"Number of images in the query directory: {len(query_keys)}")
    logging.info(f"Number of images in the reference directory: {len(reference_keys)}")

    # Find common images for evaluation
    evaluation_keys = query_keys.intersection(reference_keys)
    logging.info(f"Number of images in the evaluation set: {len(evaluation_keys)}")

    if not evaluation_keys:
        logging.error(f"No common images found in the query and reference directories.")
        return

    # Check if some images in the query directory do not have corresponding images in the reference directory
    if len(evaluation_keys) != len(query_keys) or len(evaluation_keys) != len(reference_keys):
        logging.warning("Some images in the query directory do not have corresponding images in the reference directory.")

    # Create ImageInstances for query and reference images
    queries = {
        eval_key: ImageInstance(eval_key, query_image_base_dpath)
        for eval_key in evaluation_keys}

    references = {
        eval_key: ImageInstance(eval_key, reference_image_base_dpath)
        for eval_key in evaluation_keys}

    # Boolean flag to ignore pixels with specific values
    to_ignore = var['to_ignore']
    if to_ignore:
        logging.info(f"Ignoring pixels with values: [255, 255, 255]")

    # Load quotient map if provided
    quotient_mapping = None
    if var['quotient_map_fpath']:
        try:
            quotient_mapping = load_quotient_map(var['quotient_map_fpath'])
            logging.info(f"Loaded quotient mapping from {var['quotient_map_fpath']}")
        except Exception as e:
            logging.error(f"Error loading quotient map: {str(e)}. Proceeding without quotient mapping.")

    # Create radius ranges for annulus evaluation
    min_radius = var['min_radius']
    max_radius = var['max_radius']
    step_size = var['step_size']

    if min_radius == float('inf') and max_radius == float('inf'):
        # If both are infinity, use a single range with infinity
        radius_ranges = [(float('inf'), float('inf'))]
    elif min_radius == float('inf'):
        # If only min is infinity, use a single range from infinity to max
        radius_ranges = [(float('inf'), max_radius)]
    elif max_radius == float('inf') and step_size == float('inf'):
        # If max and step are infinity, use a single range from min to infinity
        radius_ranges = [(min_radius, float('inf'))]
    else:
        # Create ranges from min to max with the given step size
        radius_ranges = [(min_radius, r) for r in np.arange(min_radius + step_size, max_radius + step_size, step_size)]
        # Add the final range to max_radius if it's not already included
        if radius_ranges[-1][1] < max_radius:
            radius_ranges.append((min_radius, max_radius))

    logging.info(f"Evaluating with radius ranges: {radius_ranges}")

    # Perform Evaluation
    match_calculator = SemanticSegmentationMatchCalculator(to_ignore=to_ignore, ignore_pixels=[255, 255, 255], quotient_mapping=quotient_mapping)
    summarizer = SummarizeMetrics()

    matches = {}
    confusion_matrix = {}
    per_image_matches = {}
    per_image_confusion_matrix = {}

    for key in evaluation_keys:
        query = queries[key]
        reference = references[key]
        
        for min_r, max_r in radius_ranges:
            match_result, confusion_matrix_result = match_calculator.match(query, reference, min_r, max_r)

            # Create a deep copy of the match_result to avoid overwriting it
            match_result_copy = copy.deepcopy(match_result)
            confusion_matrix_result_copy = copy.deepcopy(confusion_matrix_result)
            
            # Append match results to per_image_matches and Add match results to matches
            matches = dict_matches_adder(matches, match_result_copy)
            per_image_matches = dict_matches_appender(per_image_matches, match_result, f"{key}_{min_r}_{max_r}")

            # Append confusion_matrix_result to per_image_confusion_matrix and Add confusion_matrix_results to confusion_matrix
            confusion_matrix = dict_matches_adder(confusion_matrix, confusion_matrix_result_copy)
            per_image_confusion_matrix = dict_matches_appender(per_image_confusion_matrix, confusion_matrix_result, f"{key}_{min_r}_{max_r}")

    # Summarize metrics
    summarizer.summarize(matches, per_image_matches, confusion_matrix, per_image_confusion_matrix, output_filename)
    logging.info("Main function execution completed.")
    logging.info(f"Execution time: {time.time() - start_time} seconds")

if __name__ == "__main__":
    main()
