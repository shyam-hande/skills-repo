from fastapi import FastAPI
from pydantic import BaseModel
import ast
import astor

app = FastAPI()


class FileRequest(BaseModel):
    code: str


class LogInjector(ast.NodeTransformer):

    def visit_FunctionDef(self, node):
        self.generic_visit(node)

        start_log = ast.parse(
            f'logger.info("Entering {node.name}")'
        ).body[0]

        end_log = ast.parse(
            f'logger.info("Exiting {node.name}")'
        ).body[0]

        new_body = [start_log]

        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                new_body.append(end_log)
            new_body.append(stmt)

        node.body = new_body
        return node


@app.post("/inject-logs")
async def inject_logs(req: FileRequest):

    tree = ast.parse(req.code)

    transformer = LogInjector()
    transformed_tree = transformer.visit(tree)

    ast.fix_missing_locations(transformed_tree)

    modified_code = astor.to_source(transformed_tree)

    if "import logging" not in modified_code:
        modified_code = (
            "import logging\n"
            "logger = logging.getLogger(__name__)\n\n"
            + modified_code
        )

    return {
        "modified_code": modified_code
    }