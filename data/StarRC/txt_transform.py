import copy
import os

FILENAME = "/ugra/yhhan/PointNetCap/data/originFile/cc_nredu_1.txt"
CWD = os.getcwd()


NAMEMAPS = {}


def build_txtline(key_value_pairs):
    return " ".join(key_value_pairs) + "\n"


def name_map(key_value_pairs):
    if len(key_value_pairs) > 1:
        value = key_value_pairs[0]
        key = "".join(key_value_pairs[1:])
        if value.replace(" ", "") == "" or key.replace(" ", "") == "":
            return
        NAMEMAPS[key] = value
    return build_txtline(key_value_pairs)

def replace_txt(key_value_pairs):
    copy_pairs = copy.deepcopy(key_value_pairs)
    for i in range(len(key_value_pairs)):
        if key_value_pairs[i] in NAMEMAPS.keys():
            copy_pairs[i] = NAMEMAPS[key_value_pairs[i]]
    return build_txtline(copy_pairs)


    

if __name__ == "__main__":

    mode_func = {
        "NAMEMAP" : name_map,
        "REPLACE": replace_txt,
        "READ": build_txtline,
    }
    
    file_path = os.path.join(CWD, FILENAME)
    mode = "READ"
    with open(file_path, "r") as f:
        line_str = " "
        with open("/ugra/yhhan/PointNetCap/data/originFile/cc_nredu_1_output.txt", "w") as of:
            while line_str:
                line_str = f.readline()
                key_value_pairs = line_str.replace('\n', "").split(" ")
                if "*NAME_MAP" in key_value_pairs[0]:
                    mode = "NAMEMAP"
                    # print("Detected name_map, change mode {}".format(mode))
                elif key_value_pairs[0].startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9", "*D_NET")):
                    mode = "REPLACE"
                    # print("Detected content, change mode {}".format(mode))
                elif key_value_pairs[0].startswith((" ", "*CAP", "*END", "//")):
                    mode = "READ"
                    # print("Mode back to {}".format(mode))
                result_str = mode_func[mode](key_value_pairs)
                of.write(result_str)
    print("**All txt read to end!**")

