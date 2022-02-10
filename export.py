import secrets
import string
import os
import re
from email.utils import parseaddr


password = lambda length: "".join(
    [secrets.choice(string.digits + string.ascii_letters) for _ in range(length)]
)

_user_vorlage = (
    lambda name, email, kurs, sdate, edate, pw: f"""
<User Id="{name.upper()}" Language="de" Action="Insert">
  <Active><![CDATA[true]]></Active>
  <Role Id="_1" Type="Global" Action="Assign"><![CDATA[User]]></Role>
  {"".join([f'''<Role Id="_{i+2}" Type="Local" Action="Assign"><![CDATA[il_crs_member_{n}]]></Role>
''' for i,n in enumerate(kurs)])}
  <Login><![CDATA[{name.upper()}]]></Login>
  <Password Type="PLAIN">{pw}</Password>
  <Gender><![CDATA[n]]></Gender>
  <Firstname><![CDATA[{name[name.find(".")+1:]}]]></Firstname>
  <Lastname><![CDATA[{name[:name.find(".")]}]]></Lastname>
  <Email><![CDATA[{email}]]></Email>
  <TimeLimitUnlimited><![CDATA[{0 if edate != "" else 1}]]></TimeLimitUnlimited>
  {f"<TimeLimitFrom><![CDATA[{sdate} 00:00:00]]></TimeLimitFrom>" if edate else ""}
  {f"<TimeLimitUntil><![CDATA[{edate} 23:59:59]]></TimeLimitUntil>" if edate else ""}
 </User>
"""
)

_org_vorlage = (
    lambda name, orgid, role: f"""
<Assignment action='add'>
  <User id_type='ilias_login'>{name.upper()}</User>
  <OrgUnit id_type='external_id'>{orgid}</OrgUnit>
  <Role>{role}</Role>
 </Assignment>
"""
)


def _user_import(
    sname,
    email,
    kurs,
    s_count,
    l_count=0,
    sdate="",
    edate="",
):

    buffer_xml = ['<?xml version="1.0" encoding="UTF-16LE"?>\n<Users>']
    buffer_csv = ["Benutzername;Passwort\n"]
    scc = s_count.split("+")
    if len(scc) == 1:
        sc = int(scc[0])
        so = 1
    elif len(scc) == 2:
        sc = int(scc[0])
        so = int(scc[1]) + 1
    else:
        raise ValueError
    for i in range(so, so + sc):
        name = sname + ".Schueler" + str(i)
        pw = password(8)
        buffer_xml.append(_user_vorlage(name, email, kurs, sdate, edate, pw))
        buffer_csv.append(f"{name.upper()};{pw}\n")
    lcc = l_count.split("+")
    if len(lcc) == 1:
        lc = int(lcc[0])
        lo = 1
    elif len(lcc) == 2:
        lc = int(lcc[0])
        lo = int(lcc[1]) + 1
    else:
        raise ValueError
    for i in range(lo, lo + lc):
        name = sname + ".Lehrer" + str(i)
        pw = password(8)
        buffer_xml.append(_user_vorlage(name, email, kurs, sdate, edate, pw))
        buffer_csv.append(f"{name.upper()};{pw}\n")
    buffer_xml.append("\n</Users>")
    with open(f"{sname}\\{sname}_user_import.xml", "w+", encoding="UTF-16LE") as file:
        file.writelines(buffer_xml)
    with open(f"{sname}\\{sname}_login_daten.csv", "w+") as file:
        file.writelines(buffer_csv)


def _org_export(sname, s_count, l_count):
    buffer = ['<?xml version="1.0" encoding="UTF-16LE"?>\n<Assignments>']
    scc = s_count.split("+")
    if len(scc) == 1:
        sc = int(scc[0])
        so = 1
    elif len(scc) == 2:
        sc = int(scc[0])
        so = int(scc[1]) + 1
    else:
        raise ValueError
    for i in range(so, so + sc):
        name = sname + ".Schueler" + str(i)
        buffer.append(_org_vorlage(name, sname, "employee"))
    lcc = l_count.split("+")
    if len(lcc) == 1:
        lc = int(lcc[0])
        lo = 1
    elif len(lcc) == 2:
        lc = int(lcc[0])
        lo = int(lcc[1]) + 1
    else:
        raise ValueError
    for i in range(lo, lo + lc):
        name = sname + ".Lehrer" + str(i)
        buffer.append(_org_vorlage(name, sname, "superior"))
    buffer.append("\n</Assignments>")
    with open(f"{sname}\\{sname}_org_import.xml", "w+", encoding="UTF-16LE") as file:
        file.writelines(buffer)


def export(evals):
    if not os.path.isdir(evals["school"]):
        os.mkdir(evals["school"])
    try:
        if not re.match("^\\w{2,}$", evals["school"]):
            return False
        if not parseaddr(evals["sch_email"])[1]:
            return False
        if not re.match("^\\d{4}-\\d{2}-\\d{2}$", evals["vld_fr"]) and evals["vld_fr"]:
            return False
        if (
            not re.match("^\\d{4}-\\d{2}-\\d{2}$", evals["vld_utl"])
            and evals["vld_utl"]
        ):
            return False
        if evals["course"] == "Mathematik":
            course = [55948]
        elif evals["course"] == "Sprachen":
            course = []
        elif evals["course"] == "Beide":
            course = [55948]
        _user_import(
            evals["school"],
            evals["sch_email"],
            course,
            evals["st_ct"],
            evals["te_ct"],
            evals["vld_fr"],
            evals["vld_utl"],
        )
        _org_export(evals["school"], evals["st_ct"], evals["te_ct"])
        return True
    except ValueError:
        return False
