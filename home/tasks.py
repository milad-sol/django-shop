from bucket import bucket



# TODO:Can we be async
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result

def delete_bucket_objects_task(key):
    result = bucket.delete_objects(
        keys=[key]
    )
    return result