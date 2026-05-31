from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for i in data:
            if i["id"] == id:
                return jsonify(i), 200
        return {"message": "Image does not exist"}, 404

    return {"message": "internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    image_data = request.json
    if data:
        for i in data:
            if i["id"] == image_data["id"]:
                return {"Message": "picture with id {} already present".format(image_data["id"])}, 302

        data.append(image_data)
        return image_data, 201
    return {"message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    image_data = request.json
    for index, image in enumerate(data):
        if image["id"] == id:
            data[index] = image_data
            return image, 201

    return {"message": "Image not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, image in enumerate(data):
        if image["id"] == id:
            deleted_image = data.pop(id)
            return {}, 204
        
    return {"message": "picture not found"}, 404

