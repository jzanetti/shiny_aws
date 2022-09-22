from base64 import b64encode
from json import dump as json_dump
from json import load as json_load
from os import remove
from os.path import basename, join
from subprocess import Popen

cloud_init = "etc/cloud-init.sh"
spot_spec_path = "etc/spot_spec_mot.json"
spot_price = 0.1

# ----------------------------------
# Codes start from here
# ----------------------------------
with open(cloud_init, "rb") as fid:
    encoded_string = b64encode(fid.read())

decoded_string = encoded_string.decode("utf-8")

with open(spot_spec_path) as fid:
    spot_spec = json_load(fid)

spot_spec["UserData"] = decoded_string

output_json = join("/tmp", basename(spot_spec_path))

with open(output_json, 'w') as fid:
    json_dump(spot_spec, fid)

cmd = ( "aws ec2 request-spot-instances "
        f"--spot-price {spot_price} "
        "--instance-count 1 "
        f"--launch-specification file://{output_json}")
p = Popen([cmd], shell=True)
p.communicate()
remove(output_json)
