#!/usr/bin/env python
#!/usr/bin/env python
import os, eyed3, sys
import chardet

SPECIAL_CHARACTERS =    [ '!', '"', '#', '$', '%',
                        '*', '+', ',', ':', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
                        '`', '|', '~', 
                        u'À', u'Á', u'Â', u'Ã', u'È', u'É', u'Ê', u'Ì', u'Í', u'Ò', u'Ó',
                        u'Ô', u'Õ', u'Ù', u'Ú', u'Ý', u'à', u'á', u'â', u'ã', u'è', u'é',
                        u'ê', u'ì', u'í', u'ò', u'ó', u'ô', u'õ', u'ù', u'ú', u'ý', u'Ă',
                        u'ă', u'Đ', u'đ', u'Ĩ', u'ĩ', u'Ũ', u'ũ', u'Ơ', u'ơ', u'Ư', u'ư',
                        u'Ạ', u'ạ', u'Ả', u'ả', u'Ấ', u'ấ', u'Ầ', u'ầ', u'Ẩ', u'ẩ', u'Ẫ',
                        u'ẫ', u'Ậ', u'ậ', u'Ắ', u'ắ', u'Ằ', u'ằ', u'Ẳ', u'ẳ', u'Ẵ', u'ẵ',
                        u'Ặ', u'ặ', u'Ẹ', u'ẹ', u'Ẻ', u'ẻ', u'Ẽ', u'ẽ', u'Ế', u'ế', u'Ề',
                        u'ề', u'Ể', u'ể', u'Ễ', u'ễ', u'Ệ', u'ệ', u'Ỉ', u'ỉ', u'Ị', u'ị',
                        u'Ọ', u'ọ', u'Ỏ', u'ỏ', u'Ố', u'ố', u'Ồ', u'ồ', u'Ổ', u'ổ', u'Ỗ',
                        u'ỗ', u'Ộ', u'ộ', u'Ớ', u'ớ', u'Ờ', u'ờ', u'Ở', u'ở', u'Ỡ', u'ỡ',
                        u'Ợ', u'ợ', u'Ụ', u'ụ', u'Ủ', u'ủ', u'Ứ', u'ứ', u'Ừ', u'ừ', u'Ử',
                        u'ử', u'Ữ', u'ữ', u'Ự', u'ự', ]

REPLACEMENTS =          [ '\0', '\0', '\0', '\0', '\0',
                        '\0', '_', '\0', '_', '\0', '\0', '\0', '\0', '\0', '\0', '_',
                        '\0', '\0', '\0', '\0', '\0', 
                        'A', 'A', 'A', 'A', 'E', 'E', 'E', 'I', 'I', 'O', 'O',
                        'O', 'O', 'U', 'U', 'Y', 'a', 'a', 'a', 'a', 'e', 'e',
                        'e', 'i', 'i', 'o', 'o', 'o', 'o', 'u', 'u', 'y', 'A',
                        'a', 'D', 'd', 'I', 'i', 'U', 'u', 'O', 'o', 'U', 'u',
                        'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a', 'A',
                        'a', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a',
                        'A', 'a', 'E', 'e', 'E', 'e', 'E', 'e', 'E', 'e', 'E',
                        'e', 'E', 'e', 'E', 'e', 'E', 'e', 'I', 'i', 'I', 'i',
                        'O', 'o', 'O', 'o', 'O', 'o', 'O', 'o', 'O', 'o', 'O',
                        'o', 'O', 'o', 'O', 'o', 'O', 'o', 'O', 'o', 'O', 'o',
                        'O', 'o', 'U', 'u', 'U', 'u', 'U', 'u', 'U', 'u', 'U',
                        'u', 'U', 'u', 'U', 'u', ];


def remove_latin(str_input):
    str_iso = str_input.encode("ISO-8859-1")
    str_utf8 = str_iso.decode("utf-8")

    char_list = []
    for c in str_utf8:
        dc = ord(c)
        if 97 <= dc <= 122 or 65 <= dc <= 90 or 48 <= dc <= 57 or dc in [32,38,45,46]:
            char_list.append(c)
            continue
        else:
            for idx, sc in enumerate(SPECIAL_CHARACTERS):
                if ord(sc) == dc:
                    char_list.append(REPLACEMENTS[idx])
                    break

    return char_list



def remove_unicode(str_input):
    #unicode_name = unicode(str_input, "utf-8", errors="ignore"
    str_utf8 = str_input
    char_list = []
    unknown_char = 0
    for c in str_utf8:
        dc = ord(c)
        if 97 <= dc <= 122 or 65 <= dc <= 90 or 48 <= dc <= 57 or dc in [32,38,45,46]:
            char_list.append(c)
            continue
        else:
            skip = False
            for idx, sc in enumerate(SPECIAL_CHARACTERS):
                if ord(sc) == dc:
                    char_list.append(REPLACEMENTS[idx])
                    skip = True
                    break
            if skip == False:
               unknown_char = unknown_char + 1
            if (unknown_char >= 2):
                #Oop. this is not UTF-8. Change to Latin-1 now
                print "Oop. this is not UTF-8. Change to Latin-1 now"
                char_list = remove_latin(str_input)
                break

    normal_name = ''.join(char_list)
    return normal_name


def main(argv):
    path = "."
    if len(argv) > 0:
        path = argv[0]

    if not os.path.exists(path) and not os.path.isdir(path):
        print "expecting path!"
        return

    if not hasMediaFiles(path):
        print "skipping empty folder (no media files) ... "
        return

    for filename in sorted(os.listdir(path)):
        if filename.endswith('.mp3'):
            unicode_name = unicode(filename, "utf-8", errors="ignore")
            char_list = []
            for c in unicode_name:
                dc = ord(c)
                if 97 <= dc <= 122 or 65 <= dc <= 90 or 48 <= dc <= 57 or dc in [32,38,45,46]:
                    char_list.append(c)
                    continue
                else:
                    for idx, sc in enumerate(SPECIAL_CHARACTERS):
                        if ord(sc) == dc:
                            char_list.append(REPLACEMENTS[idx])
                            break

            normal_name = ''.join(char_list)
            print "File = %s" %filename
            print "New File = %s" % normal_name
            old_file = os.path.join(path ,filename)
            new_file = os.path.join(path, normal_name)
            os.rename(old_file, new_file)
    print "Normalization done."

if __name__ == "__main__":
    main(sys.argv[1:])

