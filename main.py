import os
import pathlib
import requests
from datetime import datetime
import fiftyone as fo
from requests import session

NUM_IMAGES_DOWNLOAD = 400
OLDEST_PHOTO = datetime(2000, 1, 1, 0, 0, 1)
DOWNLOAD_LOCATION = "./downloads/"
# Words or strings we don't want in the description, title, or tags
STOP_WORDS = ["sexy", "http", "cum", "horny", "sissy", "faggot", "fagot", "femboi", "anal", "pussy", "slave", "dildo", "slut", "femboi"]
FLICKR_API_KEY = os.getenv("flickr_key")


### Reset the run by deleting dataset and all previous downloaded pictures
if "flickr_pub_domain" in fo.list_datasets():
    fo.delete_dataset("flickr_pub_domain")
dataset = fo.Dataset("flickr_pub_domain", persistent=True)
# List all files in the directory
for filename in os.listdir(DOWNLOAD_LOCATION):
    file_path = os.path.join(DOWNLOAD_LOCATION, filename)

    # Check if it is a file (not a subdirectory)
    if os.path.isfile(file_path) and pathlib.Path(file_path).suffix == ".jpg":
        os.remove(file_path)  # Remove the file

def download_image(url):
    # the save as name will be everything after the last /
    # https://live.staticflickr.com/65535/54215864690_3d913dbb98.jpg
    filename = os.path.basename(url)
    full_path = DOWNLOAD_LOCATION + filename
    response = requests.get(url)

    with open(full_path, 'wb') as file:
        file.write(response.content)
    return full_path

def check_words_in_sentence(sentence):
    """Checks if any word from the array 'words' is present in the sentence.
    Args:
        sentence (str): The sentence to check.
    Returns:
        bool: True if any word is found, False otherwise.
    """
    sentence_words = sentence.lower().split()
    return any(word in sentence_words for word in STOP_WORDS)

def test_to_keep(photo):
    if datetime.strptime(photo["datetaken"], "%Y-%m-%d %H:%M:%S") > OLDEST_PHOTO:
        if len(photo["title"].split()) > 1 or len(photo["description"]["_content"].split()) > 1:
            # Extract the title, description.content, and tags and make sure there is no stop words
            if check_words_in_sentence(photo["title"] + " " + photo["description"]["_content"] + " " + photo["tags"]):
                print("Found a naughty photo: " + str(photo))
            else:
                return True
        else:
            return False

def parse_photo_field(field_name, photo_record):
    if field_name in photo_record:
        return photo_record[field_name]
    else:
        return ""

def create_sample(photo):
    # Download the photo
    file_path = download_image(photo["url_z"])
    caption = "Title: " + parse_photo_field("title", photo) + "\nDescription: " + photo["description"]["_content"]
    tags = parse_photo_field("tags", photo).split()

    sample = fo.Sample(file_path, tags=tags)
    sample["caption"] = caption
    sample["flickr_id"] = parse_photo_field("id", photo)
    sample["flickr_user"] = parse_photo_field("ownername", photo)
    sample["date_taken"] = datetime.strptime(photo["datetaken"], "%Y-%m-%d %H:%M:%S")
    sample["date_downloaded"] = datetime.now()
    sample["flickr_url"] = photo["url_z"]
    sample["woeid"] = parse_photo_field("woeid", photo)
    #Geo https://docs.voxel51.com/user_guide/using_datasets.html#geolocation
    sample["location"] = fo.GeoLocation(point=[float(photo["longitude"]), float(photo["latitude"])])
    return  sample


if __name__ == '__main__':
    print("started")
    payload = {"method": "flickr.photos.search", "license": "9,10", "safe_search": 1, "content_types":0, "format": "json", "media": "photos", "sort": "interestingness-desc"}
    payload["api_key"]= FLICKR_API_KEY
    # To understand sizing look here - https://www.flickr.com/services/api/misc.urls.html
    payload["extras"] = "description,license,date_upload,machine_tags,date_taken,owner_name,original_format,last_update,geo,tags,views,media,url_z"
    payload["nojsoncallback"] = 1
    payload["has_geo"] = 1
    payload["per_page"] = 100
    payload["page"] = 1

    # I am being lazy here and just grabbing another 250 every time even if I only need a few more to get to the desired number
    # It's fine to go over, just not by a lot. If this becomes a problem then fix
    while dataset.count() < NUM_IMAGES_DOWNLOAD:
        r = requests.get("https://www.flickr.com/services/rest/", params=payload)
        photos = r.json()["photos"]["photo"]
        samples_for_dataset = []
        for photo in photos:
            if test_to_keep(photo):
                # Make a sample and add it to the array
                sample = create_sample(photo)
                samples_for_dataset.append(sample)
        dataset.add_samples(samples_for_dataset)
        if dataset.count() >= NUM_IMAGES_DOWNLOAD:
            break
        else:
            payload["page"] = payload["page"] + 1

    session = fo.launch_app(dataset)
    session.wait()
    #dataset.save()
    print("done")