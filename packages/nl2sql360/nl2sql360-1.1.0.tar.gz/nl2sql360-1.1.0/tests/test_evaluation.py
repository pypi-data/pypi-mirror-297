from nl2sql360.core import Core
from nl2sql360.arguments import CoreArguments, EvaluationArguments

if __name__ == "__main__":
    core_args = CoreArguments()

    core = Core(core_args)

    evaluation_args = EvaluationArguments(
        eval_name="C3SQL",
        eval_dataset="spider_dev",
        eval_metrics="ex, em",
        pred_sqls_file="./C3_SQL.sql",
        enable_spider_eval=True
    )

    core.evaluate(evaluation_args)
