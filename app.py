import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import cv2
from PIL import Image
import base64
from io import BytesIO
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "The MemeMan-izator V1"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🗿📈", className="header-emoji"),
                html.H1(
                    children="The MemeMan-izator V1", className="header-title"
                ),
                html.P(
                    children="This dumb machine will replace any face on a picture with Mememan's one",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div([
            dcc.Upload(
                id='upload-image',
                children=html.Div([
                    'Drag and drop or ',
                    html.A('Select File')
                ]),
                style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-image-upload')
        ])
    ]
)


def parse_contents(contents):
    contents = str(contents)

    return html.Div([
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src='data:image/png;base64,{}'.format(contents)),
        ]),


def PIL_to_b64(image_pil):
    image_file = BytesIO()
    image_pil.save(image_file, format="PNG")
    image_bytes = image_file.getvalue()
    image_b64 = base64.b64encode(image_bytes)
    return image_b64


def b64_to_PIL(image_b64):
    image_preprocessed = image_b64.split(',')[1]
    image_bytes = base64.b64decode(image_preprocessed)
    image_file = BytesIO(image_bytes)
    image_pil = Image.open(image_file)
    return image_pil


def cv2_to_B64(image_cv2):
    print(type(image_cv2))
    image_cv2, image_array = cv2.imencode('.png', image_cv2)
    image_bytes = image_array.tobytes()
    image_b64 = base64.b64encode(image_bytes)
    return image_b64


def b64_to_Cv2(image_b64):
    image_preprocessed = image_b64.split(',')[1]
    image_bytes = base64.b64decode(image_preprocessed)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_cv2 = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)
    return image_cv2


def detect_and_replace(image_b64):
    # prepare the images
    image_pil = b64_to_PIL(image_b64)
    image_cv2 = b64_to_Cv2(image_b64)

    # create the haar cascade
    faceCascade = cv2.CascadeClassifier(
        'F:/Documents/Code/PycharmProjects/DeepLearningForFun/MemeMan-izator/haarcascade_frontalface_default.xml')

    # Read the image
    gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    bigMememanImage = Image.open('mememan.png')

    finalImage = image_pil.copy()

    for (x, y, w, h) in faces:
        # cv2.rectangle(image_cv2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        resizedMememanImage = bigMememanImage.resize((h, w))
        position = (x, y)
        finalImage.paste(resizedMememanImage, position, resizedMememanImage)
        finalImage.save('jobDone.png')

    with open("F:/Documents/Code/PycharmProjects/DeepLearningForFun/MemeMan-izator/jobDone.png", "rb") as img_file:
        b64_string = str(base64.b64encode(img_file.read()))

        correct_b64_string = b64_string[2:len(b64_string)-1]
        # correct_b64_bytes = correct_b64_string.encode('ascii')
        # base64_bytes = base64.b64encode(correct_b64_bytes)
        # correct_b64 = base64_bytes.decode('ascii')

    return correct_b64_string

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'))
def update_output(images):
    if not images:
        return

    # for i, images_str in enumerate(images):
        # image = images_str.split(',')[1]
        # data = decodebytes(image.encode('ascii'))
        # with open(f"image_{i+1}.jpg", "wb") as f:
            # f.write(data)

    children = [parse_contents(detect_and_replace(i)) for i in images]

    return children

if __name__ == "__main__":
    app.run_server(debug=True)