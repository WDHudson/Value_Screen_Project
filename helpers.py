# Group the S&P names so it's in batch requests since requesting 1 name at a time takes too much time
# Function sourced from
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]