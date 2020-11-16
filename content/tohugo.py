import os
import sys
import re

def convert_line(line):
    m = re.match("^(Title|Date|Modified|Category|Tags):(.+)$", line)
    if m:
        tpl = m.groups()
        if len(tpl)==2:
            title = tpl[0].strip().lower()
            value = tpl[1].strip()
            if title == 'title':
                return "---\ntitle: \"%s\"\n" % (value)
            if title == 'category' or title == 'tags':
                value = "[\""+value.replace(",","\",\"") +"\"]"
                title = "categories" if not title=='tags' else title
                value = value+'\n---' if title == 'tags' else value
                return "%s: %s\n" % (title, value)
            if title == 'date' or title == 'modified':
                return "%s: %s\n" % (title, value)
    r = re.compile("\[(.+)\]\(\{(.+)\}(\S+)\)")
    m = r.search(line)
    #r.match()
    while m != None:
        tpl = m.groups()
        if len(tpl) == 3:
            anchor_name = tpl[0]
            anchor_type = tpl[1]
            anchor_url = tpl[2]
            if anchor_type == 'attach' or anchor_type == 'filename':
                if ".md" in anchor_url:
                    anchor_url = anchor_url.replace(".md","/")
                #line = r.sub("[%s](../%s)" % (anchor_name, anchor_url),line,1)
                line = line.replace(m.group(),"[%s](../%s)" % (anchor_name, anchor_url),1)

        m = r.search(line, m.endpos)
    return line

def convert_file(file):
    print("Convert file: %s" % (file))
    f = open(file,'r', encoding="utf-8")
    lines = f.readlines()
    result = []
    for line in lines:
        result.append(convert_line(line))
    f.close()
    #nfile = re.sub(r"\.md", "_hugo.md", file)
    nfile = re.sub(r"\.md", ".md", file)
    print("Write file: %s" % (nfile))
    nf = open(nfile, "w", encoding="utf-8")
    nf.writelines(result)
    nf.close()

if __name__ == '__main__':
    for path, dirname, fnames in os.walk("."):
        if not path.startswith(".\.git"):
            for filename in fnames:
                fname = os.path.join(path,filename)
                if fname.endswith(".md") and not fname.endswith("_hugo.md"):
                    convert_file(fname)
