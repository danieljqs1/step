from flask import Flask, request, Response
import requests
import cadquery as cq
import tempfile

app = Flask(__name__)

@app.route('/convert_step_to_stl', methods=['POST'])
def convert_step_to_stl():
    try:
        # Check if a file was included in the request
        if 'file' not in request.files:
            return "No file provided in the request.", 400

        file = request.files['file']

        # Check if the file has a valid name and extension
        if file.filename == '':
            return "No selected file.", 400

        if file:
            # Create a temporary file to save the uploaded STEP file
            step_file = tempfile.NamedTemporaryFile(delete=False, suffix=".stp")
            step_file_path = step_file.name
            file.save(step_file_path)

            # Load the uploaded STEP file and convert it to a CadQuery object
            cad_part = cq.importers.importStep(step_file_path)

            # Check if the cad_part is not empty and contains geometry
            if cad_part:
                # Export the CadQuery object to STL format
                stl_file = tempfile.NamedTemporaryFile(delete=False, suffix=".stl")
                stl_file_path = stl_file.name
                cad_part.val().exportStl(stl_file_path)

                # Create a Flask response with the STL content
                stl_response = Response(open(stl_file_path, 'rb').read(), content_type='application/sla')
                stl_response.headers['Content-Disposition'] = f'attachment; filename=output.stl'

                return stl_response
            else:
                # Handle the case where cad_part is empty or invalid
                return "Invalid or empty CadQuery object.", 400
        else:
            return "Failed to process the uploaded file.", 400
    except Exception as e:
        return str(e), 500
