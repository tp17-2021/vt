import json
import os


def get_config():
    os.chdir('/code/')

    with open(os.path.join(os.getcwd(), 'src/public/config.json'), 'rb') as f:
        data = json.load(f)

    return data

async def transform_vote_to_print(vote: dict) -> dict:

    print("This is trasforming vote before transform")
    print(vote)
    data = get_config()
    
    res_dict = {}
    res_dict['title'] = "Voľby do národnej rady"
    res_dict["candidates"] = []
    res_dict["party"] = "---"

    for party in data["parties"]:
        if party["_id"] == vote["party_id"]:
            res_dict["party"] = party["name"]

            for candidate in party["candidates"]:
                if candidate["_id"] in vote["candidate_ids"]:
                    name = str(candidate["order"]) +". "+ candidate["first_name"] +" "+ candidate["last_name"]
                    res_dict["candidates"].append(name)

    print("Vote to print:", res_dict)
    
    return res_dict