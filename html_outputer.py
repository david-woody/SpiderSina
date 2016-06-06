import db_helper


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []
        self.dbhelper = db_helper.DBclient()
        self.dbcollection = self.dbhelper.get_collection("baidu")

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = open('output.html', 'w')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
            fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
            fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")

    def output_dbs(self):
        for data in self.datas:
            self.dbhelper.insert_one_doc(self.dbcollection, data)
