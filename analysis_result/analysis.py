import sys
import re
origin_txt = sys.argv[1]
segmented_txt = sys.argv[2]

with open(origin_txt,"r") as f:
    lines_origin = f.readlines()
f.close()

with open(segmented_txt,"r") as f2:
    lines_segmented = f2.readlines()
f2.close()

def char_in_which_word(loc_from,loc_to,seg_word):
    if loc_from == 0:
        if len(seg_word[0]) == loc_to:
            return True
    else:
        letter_contained = 0
        cursor = 0
        flag = False
        for i in range(len(seg_word)):
            cursor = letter_contained
            letter_contained += len(seg_word[i])
            if letter_contained < loc_from:
                continue
            if letter_contained > loc_to:
                break
            if cursor<= loc_from and letter_contained >=loc_from:
                tmp = i
            if cursor<=loc_to and letter_contained >=loc_to:
                if i == tmp:
                    if cursor == loc_from and letter_contained == loc_to:
#print seg_word[i]
                        flag = True;
        return flag

def split_position(word_list):
    split_loc = []
    len_split = 0
    for i in range(len(word_list)):
        len_split += len(word_list[i])
        split_loc.append((len_split-1,len_split))
    return split_loc  

def word_based_analysis(str1,str2):
    word_in_origin = str1.split()
    word_in_segmented = str2.split()
    no_space_line = re.sub(r'\s+','',str1)
#    print word_in_origin
#    print word_in_segmented
    word_in_total_origin = len(word_in_origin)
    word_found = len(word_in_segmented)
    letter_contained = 0
    cursor = 0
    correct_found_word = 0
    for i in range(len(word_in_origin)):
        cursor = letter_contained
        letter_contained += len(word_in_origin[i])
        ret = char_in_which_word(cursor,letter_contained,word_in_segmented)
        if ret == True:
            correct_found_word += 1
    return (correct_found_word,word_found,word_in_total_origin)

def split_based_analysis(str1,str2):
    word_in_origin = str1.split()
    word_in_segmented = str2.split()
    split_loc_origin = split_position(word_in_origin)
    split_loc_segment = split_position(word_in_segmented)
    correct_found_split = 0
#    print split_loc_origin
#    print split_loc_segment
    for i in split_loc_segment:
        if i in split_loc_origin:
#print i
            correct_found_split += 1
    correct_found_split -= 1
    return (correct_found_split,split_loc_origin,split_loc_segment)


def bracket_miss_in_middle(split_origin,split_segment): 
    correct_both_side = 0
    correct_left_side = 0
    correct_right_side = 0
    correct_neither_side = 0
    split_origin.append((0,0))
    split_segment.append((0,0))
    split_origin = sorted(split_origin)
    split_segment = sorted(split_segment)
    for i in range(len(split_segment)):
        if i != 0 and i != len(split_segment)-1:
            if split_segment[i] in split_origin:
                tmp = split_origin.index(split_segment[i])
                if split_segment[i-1] in split_origin and split_segment[i+1] in split_origin:
                    tmp2 = split_origin.index(split_segment[i-1])
                    tmp3 = split_origin.index(split_segment[i+1])
                    if tmp2 == tmp-1 and tmp3 == tmp + 1:
                        correct_both_side += 1
                elif split_segment[i-1] not in split_origin and split_segment[i+1] not in split_origin:
                    correct_neither_side += 1
                elif split_segment[i-1] in split_origin:
                    tmp2 = split_origin.index(split_segment[i-1])
                    if tmp2 == tmp - 1:
                        correct_left_side += 1
                else:
                    tmp3 = split_origin.index(split_segment[i+1])
                    if tmp3 == tmp + 1:
                        correct_right_side += 1
    return (correct_both_side,correct_left_side,correct_right_side,correct_neither_side)

if __name__ == '__main__':
    lines_num = len(lines_origin)
    correct_found_word = 0
    found_word = 0
    total_word_in_origin = 0
    correct_found_split = 0
    found_split = 0
    total_split_in_origin = 0
    correct_both_side = 0
    correct_left_side = 0
    correct_right_side = 0
    correct_neither_side = 0
    for i in range(lines_num):
        x, y,z = word_based_analysis(lines_origin[i],lines_segmented[i])
        correct_found_word += x
        found_word += y
        total_word_in_origin += z
        p,q,r = split_based_analysis(lines_origin[i],lines_segmented[i])
        correct_found_split += p
        found_split += len(r)
        total_split_in_origin += len(q)
        a,b,c,d = bracket_miss_in_middle(q,r)
        correct_both_side += a
        correct_left_side += b
        correct_right_side += c
        correct_neither_side += d
    print "word-based precision %.10f"%(correct_found_word/float(found_word))
    print "word_based recall %.10f"%(correct_found_word/float(total_word_in_origin)) 
    print "split-based precision %.10f"%(correct_found_split/float(found_split))
    print "split_based recall %.10f"%(correct_found_split/float(total_split_in_origin))
    print "total_split_in_origin %d"%(total_split_in_origin)
    print "correct_both_side %d"%(correct_both_side)
    print "correct_left_side %d"%(correct_left_side)
    print "correct_right_side %d"%(correct_right_side)
    print "correct_neither_side %d"%(correct_neither_side)    
