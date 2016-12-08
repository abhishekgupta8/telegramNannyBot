import subprocess

#XXX remove hard coding for DBC, scriptPath, reportPath
class CoreSummary(object):
   def __init__(self, pr, sb):
      self.pr = pr
      self.sb = sb
      self.dbc = "gabhishek@pa-dbc1128.eng.vmware.com"
      self.scriptPath = "/dbc/pa-dbc1128/gabhishek/debug/coresummary_report.py"
      self.reportPath = "/Users/gabhishek/mount_point/debug"

   def run_report(self):
      cmd = "ssh %s \"python %s -p %s -s %s\"" % (self.dbc, self.scriptPath, self.pr, self.sb)
      output = subprocess.check_output(cmd, shell=True)
      if "Error" in output:
         return output
      else:
         report_html = output
      report_txt_name = "%s_report.txt" % self.pr
      report_txt_path = "%s/%s" % (self.reportPath, report_txt_name)
      report_txt_fp = open(report_txt_path, 'r')
      report_txt = report_txt_fp.read()
      summary = report_txt
      summary += "Use this link for detailed core summary\n"
      summary += report_html
      return summary

if __name__ == '__main__':
   test = CoreSumamry("1491660", "Dec-02-vmkernel-zdump.1.gz")
   test.run_report()
