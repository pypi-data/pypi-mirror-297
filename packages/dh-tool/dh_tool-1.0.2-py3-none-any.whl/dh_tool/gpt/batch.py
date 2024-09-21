import openai
from dh_tool.common import *


class BatchProcessor:
    def __init__(self, api_key) -> None:
        self.client = openai.OpenAI(api_key=api_key)
        self.save_dir = "./gpt_batchs"

    def request_batch(self, batchs, description):
        save_dir = Path(self.save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        tmp_dir = save_dir / "tmp.jsonl"

        with tmp_dir.open("wt", encoding="utf-8") as f:
            f.writelines(
                [json.dumps(b, ensure_ascii=False, indent=None) + "\n" for b in batchs]
            )

        batch_file = self.client.files.create(file=open(tmp_dir, "rb"), purpose="batch")

        tmp_dir.unlink()

        response = self.client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={"description": description},
        )

        batch_path = save_dir / response.id
        batch_path.mkdir(parents=True, exist_ok=True)

        with (batch_path / "input.jsonl").open("wt", encoding="utf-8") as f:
            f.writelines(
                [json.dumps(b, ensure_ascii=False, indent=None) + "\n" for b in batchs]
            )

        retrieved = json.loads(
            self.client.batches.retrieve(response.id).model_dump_json()
        )
        with (batch_path / "information.json").open("wt", encoding="utf-8") as f:
            json.dump(retrieved, f, ensure_ascii=False, indent=4)

        return retrieved

    def check_batch(self, batch_id):
        result_list = json.loads(self.client.batches.list(limit=100).model_dump_json())[
            "data"
        ]
        result = [i for i in result_list if i["id"] == batch_id][0]
        if result["status"] == "completed":
            self.save_batch_result(result)
            print("배치 결과 완료!")

        else:
            print("배치 완료 아직 안됨")
            print(result)

    def save_batch_result(self, result, save_dir=".batchs"):
        output_file_id = result["output_file_id"]
        content = self.client.files.content(output_file_id)
        save_path = Path(save_dir) / result["id"]
        result_path = save_path / "result.jsonl"
        if result_path.exists():
            print(f"이미 {result_path}에 저장되어 있음")
            return

        content_str = content.read().decode()
        # 각 라인을 개별적으로 파싱한 후 저장
        lines = content_str.splitlines()
        parsed_lines = [json.loads(line) for line in lines]

        # 유니코드 이스케이프 없이 JSONLines 형식으로 저장
        with result_path.open("wt", encoding="utf-8") as f:
            for parsed_line in parsed_lines:
                f.write(json.dumps(parsed_line, ensure_ascii=False) + "\n")

    def make_batch(self, completed_prompts):
        if isinstance(completed_prompts, str):
            completed_prompts = [completed_prompts]
        batchs = [self.batch_format(prompt) for prompt in completed_prompts]
        return batchs

    def batch_format(self, custom_id, prompt, **gpt_params):
        batch_format = {
            "custom_id": custom_id,
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-4o",
                "messages": [
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 4096,
                "temperature": 0,
                "seed": 1,
            },
        }
        if gpt_params:
            batch_format["body"].update(gpt_params)
        return batch_format
