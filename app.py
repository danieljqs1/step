from flask import Flask, request, Response
import requests
import cadquery as cq

app = Flask(__name__)

@app.route('/convert_step_to_stl', methods=['GET'])
def convert_step_to_stl():
    try:
        # Get the URL parameter from the request
        url = request.args.get('url')
        # Check if the URL parameter is provided
        if url is None:
            return "Please provide a 'url' parameter in the query string.", 400
        # Fetch the STEP file from the URL using requests
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Read the STEP file using CadQuery
            cad_part = cq.importers.importStep(response.content)
            # Convert the CadQuery part to an STL mesh
            stl_mesh = cad_part.val().exportStlString()
            # Create a Flask response with the STL content
            stl_response = Response(stl_mesh, content_type='application/sla')
            # Set the file name in the Content-Disposition header as an attachment
            stl_response.headers['Content-Disposition'] = f'attachment; filename={url.split("/")[-1]}.stl'
            return stl_response
        return f"Failed to fetch or convert the STEP file from URL: {url}", response.status_code
    except Exception as e:
        return str(e), 500
