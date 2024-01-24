""" Spider evaluation script. """

import subprocess
import argparse
import json
import os
import logging


def run_the_benchmark():
    """
    Run the benchmark by sampling the Spider dataset and generating SQL queries for evaluation.
    This function takes no arguments and does not return any values.
    """
    parser = argparse.ArgumentParser(description="Create a sampled version of the Spider dataset.")

    parser.add_argument('--spider-data-dir', 
                        type=str, 
                        required=True, 
                        help="""Path to the Spider dataset directory. 
                        This directory should contain the train.json, dev.json, and databases, 
                        downloaded from https://yale-lily.github.io/spider.""")

    parser.add_argument('--sample-data-dir', 
                        type=str, 
                        required=True, 
                        help="Path to the output directory of the sampled benchmark.")
    
    parser.add_argument('--sample-pred-dir', 
                        type=str, 
                        required=True, 
                        help="Path to the directory of generated SQL files.")

    parser.add_argument('--sample-factor', 
                        type=float, 
                        required=True, 
                        help="The sample factor to apply to sample a fraction of examples in both the train and dev datasets.")

    parser.add_argument('--model', 
                        type=str, 
                        required=True, 
                        help="The model to use for generating SQL queries.")

    args = parser.parse_args()

    logging.getLogger("root").setLevel(logging.WARNING)

    if 'OPENAI_API_KEY' in os.environ:
        print("OPENAI_API_KEY is set")
    else:
        print("OPENAI_API_KEY is not set")
        with open('../api_info/api_info.json', 'r', encoding='utf-8') as f:
            api_info = json.load(f)
            
            os.environ['OPENAI_API_KEY'] = api_info.get('openai_api_key')

    try:
        result = subprocess.run(
            ['python', 'sample_benchmark.py', 
            '--input', args.spider_data_dir, 
            '--output', args.sample_data_dir, 
            '--sample-factor', str(args.sample_factor)
            ],
            check=True,  # Raises CalledProcessError if the command exits with a non-zero status
            text=True,   # Capture output as a string rather than as bytes
            capture_output=True  # Capture stdout and stderr from the command
        )
        print(result.stdout)  # Print the standard output from the command
    except subprocess.CalledProcessError as e:
        print("An error occurred while trying to run the command.")
        print(f"Exit code: {e.returncode}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")


    try:
        result = subprocess.run(
            ['python', 'generate_sql.py', 
             '--input', args.sample_data_dir, 
             '--output', args.sample_pred_dir, 
             '--model', args.model
             ],
            check=True,  # Raises CalledProcessError if the command exits with a non-zero status
            text=True,   # Capture output as a string rather than as bytes
            capture_output=True  # Capture stdout and stderr from the command
        )
        print(result.stdout)  # Print the standard output from the command
    except subprocess.CalledProcessError as e:
        print("An error occurred while trying to run the command.")
        print(f"Exit code: {e.returncode}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")

    try:
        result = subprocess.run(
            ['python', 'evaluate.py', 
             '--spider-dir', args.sample_data_dir,
            '--predict-dir', args.sample_pred_dir, 
            '--model', args.model],
            check=True,  # Raises CalledProcessError if the command exits with a non-zero status
            text=True,   # Capture output as a string rather than as bytes
            capture_output=True  # Capture stdout and stderr from the command
        )
        print(result.stdout)  # Print the standard output from the command
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to run the command: {e}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")

if __name__ == '__main__':
    run_the_benchmark()
