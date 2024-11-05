output = '''<file_write>FILE_PATH: /Users/a11/Desktop/MetaAgent/MetaAgent/mlbench/test1.json CONTENT: { "name": "John", "age": 30, "city": "New York" }</file_write>'''
if "<file_write>" in output:
                # 提取文件路径和内容，然后将内容保存到文件路径
                file_path = output.split("<file_write>")[-1]
                file_path = file_path.split("</file_write>")[0]
                file_path = file_path.split("FILE_PATH:")[1]
                file_path = file_path.split("CONTENT:")[0]
                file_path = file_path.replace(" ", "")
                file_content = output.split("CONTENT:")[1]
                file_content = file_content.split("</file_write>")[0]
                file_content = file_content.replace(" ", "")
                
                # 确保文件路径存在
                import os
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, "w") as f:
                    f.write(file_content)
                action = None