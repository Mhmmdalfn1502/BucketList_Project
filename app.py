from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://mhmmdalfn1502:ALFAN@cluster0.hh8koxv.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
)
db = client.Data

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {"num": num, "bucket": bucket_receive, "done": 0}
    db.bucket.insert_one(doc)
    return jsonify({"msg": "Data Save"})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.bucket.update_one({"num": int(num_receive)}, {"$set": {"done": 1}})
    return jsonify({"msg": "Update Done!"})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {"_id": False}))
    return jsonify({"buckets": buckets_list})


@app.route("/delete", methods=["POST"])
def delete_bucket_item():
    num_receive = request.form["num_give"]
    # Hapus item dengan nomor yang sesuai dari database
    db.bucket.delete_one({"num": int(num_receive)})
    return jsonify({"msg": "Item berhasil dihapus"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
