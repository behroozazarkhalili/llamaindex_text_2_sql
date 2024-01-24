# Evaluation using Spider Text-to-SQL Dataset

We are going to benchmark LlamaIndex's performance for complex queries on multiple domains.
Therefore, we define this project to measure how each iteration of LLM improves its Text-to-SQL capability.

## How one can use this repo?

1. Download [benchmark dataset](https://yale-lily.github.io/spider),
   
2. Use `sample_benchmark.py` to sample the benchmark dataset so we don't spend too much money when testing. Skip this step when running the complete benchmark.

```bash
python sample_benchmark.py --input <benchmark path> --output spider-0_001 --sample-factor 0.001
# A smaller benchmark with 1/1000 examples is saved in directory spider-0_001, which we use as our benchmark for testing purpose.
```

3. Use `generate_sql.py` to generate the predicted SQL queries given the input benchmark.

```bash
python generate_sql.py --input spider-0_001 --output spider-0_001-pred --model gpt-3.5-turbo
# Predicted SQLs are saved in the output directory.
```

4. Use `evaluate.py` to evaluate the generated SQLs against
   golden SQLs by matching the natural language answers generated from their
   respective execution outputs. This is called [Answer Accuracy](https://ekzhu.medium.com/human-aligned-text-to-sql-evaluation-399123fa0a64).

```bash
python evaluate.py --spider-dir spider-0_001 --predict-dir spider-0_001-pred \
    --model gpt-3.5-turbo
```

This will produce two JSON files `train_eval.json` and `dev_eval.json` with
the evaluation results in the `--predict-dir` directory.


Or you can simply run the following code to run all scripts altogether.

```bash
python3 main.py --spider-data-dir ../data/spider --sample-data-dir ../data/spider-0_001 --sample-factor 0.001 --sample-pred-dir ../data/spider-0_001-pred --model gpt-4
```
## Result

Based on 0.999 of samples from Spider benchmark.

| Model            | Answer Accuracy |
| ---------------- | --------------- |
| gpt-3.5-turbo    | 0.8042          |
| gpt-4            | 0.8058          |

## TODO

1. Auto-course-correction encountering SQL errors using agent.
2. Use training set to generate in-context learning examples.