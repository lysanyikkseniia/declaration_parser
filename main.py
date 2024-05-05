from program import Program

program1 = Program(file_path='example1.kt')
data_json1 = program1.export_declarations_to_json('output1.json')

program2 = Program(file_path='example2.kt')
data_json2 = program2.export_declarations_to_json('output2.json')
