#!/usr/bin/env python

import argparse
import json
import bson
from gesund_val_library.utils.io_utils import read_json, save_plot_metrics_as_json, format_metrics
from gesund_val_library.utils.coco_converter import COCOConverter

from gesund_val_library.scripts.problem_type_factory import get_validation_creation
import os

def main():
    parser = argparse.ArgumentParser(description='Run validation metrics calculation.')
    parser.add_argument('--annotations', type=str, required=True, help='Path to the JSON file with annotations.')
    parser.add_argument('--predictions', type=str, required=True, help='Path to the JSON file with predictions.')
    parser.add_argument('--class_mappings', type=str, required=True, help='Path to the JSON file with class mappings.')
    parser.add_argument('--problem_type', type=str, required=True,
                        choices=['classification', 'semantic_segmentation', 'instance_segmentation', 'object_detection'],
                        help='The type of problem (only classification at the moment).')

    args = parser.parse_args()

    # Load JSON files
    try:
        successful_batch_data = read_json(args.predictions)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading predictions file: {e}")
        return

    try:
        annotation_data = read_json(args.annotations)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading annotations file: {e}")
        return

    try:
        class_mappings = read_json(args.class_mappings)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading class mappings file: {e}")
        return

    # Get the appropriate ValidationCreation class for the problem type
    batch_job_id = str(bson.ObjectId())
    output_dir = os.path.join("outputs", batch_job_id)
    
    # Check and convert annotations if necessary
    converter_annot = COCOConverter(annotations=annotation_data)
    if converter_annot.is_annot_coco_format():
        annotation_data = converter_annot.convert_annot_if_needed()
        
    converter_pred = COCOConverter(successful_batch_data=successful_batch_data)
    if converter_pred.is_pred_coco_format():
        successful_batch_data = converter_pred.convert_pred_if_needed()

    
    ValidationCreationClass = get_validation_creation(args.problem_type)
    validation = ValidationCreationClass(batch_job_id)
    
    try:
        validation_data = validation.create_validation_collection_data(successful_batch_data, annotation_data)
        metrics = validation.load(validation_data, class_mappings)
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return

    # Print the metrics data
    format_metrics(metrics)

    # Saving each plot's metrics as individual JSON files
    save_plot_metrics_as_json(metrics, output_dir)

if __name__ == "__main__":
    main()
