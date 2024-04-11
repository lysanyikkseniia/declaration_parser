from program import Program

program = Program(file_path='example.kt')

data_json = program.export_declarations_to_json('hiii.json')
