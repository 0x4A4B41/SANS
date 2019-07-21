import mysql.connector
from CapstoneBackend.Rested.Config.DatabaseCreds import DatabaseCreds

from CapstoneBackend.Rested.Base import Common


class dump_wireshark_oui_in_sql:


    @staticmethod
    def dump_wireshark_oui_to_db():

        c = Common()
        wire_shark_oui_list = c.retrieve_oui_table_wireshark()
        print(len(wire_shark_oui_list))

        conn = mysql.connector.connect(
            user=DatabaseCreds.CapstoneDev.user,
            password=DatabaseCreds.CapstoneDev.password,
            host=DatabaseCreds.CapstoneDev.host,
            database='CapStone'
        )
        cur = conn.cursor()
        for mac_addr_obj in wire_shark_oui_list:
            sql = "insert into ouiTbl(oui,shortName,longName) VALUES (%s,%s,%s)"
            data = (str(mac_addr_obj.get_mac_oui().strip()), str(mac_addr_obj.get_short_name()).strip(),
                    str(mac_addr_obj.get_long_name()).strip())
            try:
                cur.execute(sql, data)
                conn.commit()
            except mysql.connector.errors.IntegrityError:
                pass
            except mysql.connector.errors.DatabaseError:
                print("SQL:" + str(sql))
                print("Data:" + str(data))

        cur.close()
        conn.close()


if __name__ == '__main__':
    dump_wireshark_oui_in_sql.dump_wireshark_oui_to_db()
