import click
from mimir import create_qna, eval_rag


@click.group(name="mimir")
def cli():
    """CLI tool for QnA creation and RAG model evaluation."""
    pass


@click.command()
@click.argument("num_tests", type=int, required=True)
@click.argument("data_dir", type=str, required=True)
@click.argument("output_json_file", type=str, required=True)
def gen(num_tests, data_dir, output_json_file):
    """Create sample QnA given a corpus of PDF documents."""
    create_qna(num_tests, data_dir, output_json_file)
    click.echo(f"QnA created and saved to {output_json_file}")


@click.command()
@click.argument("generate_qna_file_path", type=str, required=True)
@click.argument("rag_qna_file_path", type=str, required=True)
def eval(generate_qna_file_path, rag_qna_file_path):
    """Evaluate the RAG model."""
    eval_rag(generate_qna_file_path, rag_qna_file_path)


cli.add_command(gen)
cli.add_command(eval)

if __name__ == "__main__":
    cli()
