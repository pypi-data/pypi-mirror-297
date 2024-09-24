# eval

![Lint](https://github.com/instructlab/eval/actions/workflows/lint.yml/badge.svg?branch=main)
![Build](https://github.com/instructlab/eval/actions/workflows/pypi.yaml/badge.svg?branch=main)
![Release](https://img.shields.io/github/v/release/instructlab/eval)
![License](https://img.shields.io/github/license/instructlab/eval)

Python Library for Evaluation

## MT-Bench / MT-Bench-Branch Testing Steps

> **⚠️ Note:** Must use Python version 3.10 or later.

```shell
# Optional: Use cloud-instance.sh (https://github.com/instructlab/instructlab/tree/main/scripts/infra) to launch and setup the instance
scripts/infra/cloud-instance.sh ec2 launch -t g5.4xlarge
scripts/infra/cloud-instance.sh ec2 setup-rh-devenv
scripts/infra/cloud-instance.sh ec2 install-rh-nvidia-drivers
scripts/infra/cloud-instance.sh ec2 ssh sudo reboot
scripts/infra/cloud-instance.sh ec2 ssh


# Regardless of how you setup your instance
git clone https://github.com/instructlab/taxonomy.git && pushd taxonomy && git branch rc && popd
git clone --bare https://github.com/instructlab/eval.git && git clone eval.git/ && cd eval && git remote add syncrepo ../eval.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
pip install vllm
python -m vllm.entrypoints.openai.api_server --model instructlab/granite-7b-lab --tensor-parallel-size 1
```

In another shell window

```shell
export INSTRUCTLAB_EVAL_FIRST_N_QUESTIONS=10 # Optional if you want to shorten run times
# Commands relative to eval directory
python3 tests/test_gen_answers.py
python3 tests/test_branch_gen_answers.py
```

Example output tree

```shell
eval_output/
├── mt_bench
│   └── model_answer
│       └── instructlab
│           └── granite-7b-lab.jsonl
└── mt_bench_branch
    ├── main
    │   ├── model_answer
    │   │   └── instructlab
    │   │       └── granite-7b-lab.jsonl
    │   ├── question.jsonl
    │   └── reference_answer
    │       └── instructlab
    │           └── granite-7b-lab.jsonl
    └── rc
        ├── model_answer
        │   └── instructlab
        │       └── granite-7b-lab.jsonl
        ├── question.jsonl
        └── reference_answer
            └── instructlab
                └── granite-7b-lab.jsonl
```

```shell
python3 tests/test_judge_answers.py
python3 tests/test_branch_judge_answers.py
```

Example output tree

```shell
eval_output/
├── mt_bench
│   ├── model_answer
│   │   └── instructlab
│   │       └── granite-7b-lab.jsonl
│   └── model_judgment
│       └── instructlab
│           └── granite-7b-lab_single.jsonl
└── mt_bench_branch
    ├── main
    │   ├── model_answer
    │   │   └── instructlab
    │   │       └── granite-7b-lab.jsonl
    │   ├── model_judgment
    │   │   └── instructlab
    │   │       └── granite-7b-lab_single.jsonl
    │   ├── question.jsonl
    │   └── reference_answer
    │       └── instructlab
    │           └── granite-7b-lab.jsonl
    └── rc
        ├── model_answer
        │   └── instructlab
        │       └── granite-7b-lab.jsonl
        ├── model_judgment
        │   └── instructlab
        │       └── granite-7b-lab_single.jsonl
        ├── question.jsonl
        └── reference_answer
            └── instructlab
                └── granite-7b-lab.jsonl
```
