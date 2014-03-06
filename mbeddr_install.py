# THE WAY TO RUN THE NEWEST SCRIPT VERSION

#bash command to run it
#mi=`mktemp` && wget -nv https://raw.github.com/qutorial/mbeddr_python_installer/master/mbeddr_install.py -O $mi && python2.7 $mi; rm $mi;

################### -- CONFIGURATION -- ###################

# MPS CONFIGURATION

EAPNum = "27"  
MPSSourceUrl = """http://download-ln.jetbrains.com/mps/31/"""
MPSWin = """MPS-3.1-EAP1-"""+EAPNum+""".exe"""
MPSMac = """MPS-3.1-EAP1-"""+EAPNum+"""-macos.dmg"""
MPSLin = """MPS-3.1-EAP1-"""+EAPNum+""".tar.gz"""
MPSZip = """MPS-3.1-EAP1-"""+EAPNum+""".zip"""
MPSArcDir = """MPS 3.1 EAP"""

MPS_VMOPTIONS="""-client
-Xss1024k
-ea
-Xmx2100m
-XX:MaxPermSize=2256m
-XX:NewSize=512m
-XX:+HeapDumpOnOutOfMemoryError
-Dfile.encoding=UTF-8
-Dapple.awt.graphics.UseQuartz=true
-Didea.paths.selector=MPS30
-Didea.config.path=IdeaConfig
-Didea.system.path=IdeaSystem"""
#-Didea.plugins.path=IdeaPlugins"""

LIBRARY_MANAGER = """<?xml version="1.0" encoding="UTF-8"?>
<application>
  <component name="LibraryManager">
    <option name="libraries">
      <map>
        <entry key="mbeddr.core">
          <value>
            <Library>
              <option name="name" value="mbeddr.core" />
              <option name="path" value="${mbeddr.github.core.home}/code" />
            </Library>
          </value>
        </entry>
      </map>
    </option>
  </component>
</application>"""

PATH_MACROS = """<?xml version="1.0" encoding="UTF-8"?>
<application>
  <component name="PathMacrosImpl">
    <macro name="mbeddr.github.core.home" value="MbeddrDir" />
  </component>
</application>
"""


# CBMC CONFIGURATION
CBMCVersion="""4"""
CBMCSubVersion = """7"""
CBMC32BitLinuxUrl = """http://www.cprover.org/cbmc/download/cbmc-""" + CBMCVersion + "-" + CBMCSubVersion + """-linux-32.tgz"""
CBMC64BitLinuxUrl = """http://www.cprover.org/cbmc/download/cbmc-""" + CBMCVersion + "-" + CBMCSubVersion + """-linux-64.tgz"""
CBMCMacFileName = """cbmc-""" + CBMCVersion + "-" + CBMCSubVersion + """.pkg"""
CBMCMacUrl = """http://www.cprover.org/cbmc/download/""" + CBMCMacFileName;
CBMCInstallDir = "/usr/bin"



# MBEDDR CONFIGURATION
MbeddrRepo = """https://github.com/mbeddr/mbeddr.core.git"""
TheBranch = "fortissStable"
BUILD_PROPERTIES = """# MPS installation
mps.home=MPSDir
# Folder where MPS stores it's cache
mps.platform.caches=MPSCaches
# Points to the root folder of the mbeddr.core repository
mbeddr.github.core.home=MbeddrDir
"""



# JAVA CONFIGURATION
InstallJavaMessage= """Please, install a Java (R, TM) from Oracle. 

http://www.oracle.com/technetwork/java/javase/downloads/index.html"""



InstallJavaHintUbuntu = """\nOn Ubuntu this might work:
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java7-installer
"""

# ANT CONFIGURATION
InstallAntMessage= """Please, install Apache Ant(TM).\n 

http://ant.apache.org/bindownload.cgi

On Ubuntu this might work:
sudo apt-get install ant
"""


# GIT CONFIGURATION
InstallGitMessage= """Please, install Git.\n 

http://git-scm.com/downloads

On Ubuntu this might work:
sudo apt-get install git
"""

################### END OF CONFIGURATION ###################

import sys, os, subprocess, urllib2, platform, tarfile
from os.path import expanduser
import zipfile, tarfile
import os.path

# Checking Python

if sys.version_info < (2, 7):
    print "Your Python version is old. Please, install Python 2.7."
    print "http://www.python.org/download/"
    print "Run the script like this afterwards: python2.7 "+os.path.basename(__file__)
    exit(1);

# Detecting OS
    
def getOs():
  s = platform.platform()
  if "Lin" in s:
    if platform.architecture()[0] == '64bit':
      return "Lin64"
    else:
      return "Lin32";
  if "Darwin" in s:
    return "Mac"
  if "Win" in s:
    return "Win"
    
    
# Downloading file with progress

def downloadFile(url, destdir):
  file_name = url.split('/')[-1]
  u = urllib2.urlopen(url)
  resName = os.path.join(destdir, file_name)
  f = open(resName, 'wb')
  meta = u.info()
  file_size = int(meta.getheaders("Content-Length")[0])
  print "Downloading: %s Bytes: %s" % (file_name, file_size)

  file_size_dl = 0
  block_sz = 8192
  while True:
      buffer = u.read(block_sz)
      if not buffer:
	  break

      file_size_dl += len(buffer)
      f.write(buffer)
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
      status = status + chr(8)*(len(status)+1)
      print status,

  f.close()
  
  print "\n"
  
  return resName
    
# Unarchiving Zips and Tars

def unzip(zipzip, dest):
  zfile = zipfile.ZipFile(zipzip)
  for name in zfile.namelist():
    (dirname, filename) = os.path.split(name)
    print "Decompressing " + filename + " on " + dirname
    if not os.path.exists(dirname):
      os.makedirs(dirname)
    zfile.extract(name, os.path.join(dest,dirname))

def untgz(arc, dest):
  tfile = tarfile.open(arc, 'r:gz');
  tfile.extractall(dest);
  
def unarchive(a, dest):
  if "zip" in a:
    unzip(a, dest);
  else:
    untgz(a, dest);

    
# GIT 

def checkGitVersion(git):
  if "git version" in git:
    return True;
  else:
    return "Unrecognized git version\n"    
   
def checkGit():  
  try:
    git = subprocess.check_output(["git", "--version"], stderr=subprocess.STDOUT)
    return checkGitVersion(git)
  except OSError:
    return InstallGitMessage;

    
# JAVA 

def checkJavaVersion(java):
  vals = java.split() 
  a = [s for s in vals if "1.6" in s]
  b = [s for s in vals if "1.7" in s]
  c = [s for s in vals if "HotSpot" in s]
  if len(c) > 0:
    if len(a) + len(b) > 0:
      return True;
  answer = "Java version is not recognized\n"+InstallJavaMessage;
  if "Lin" in getOs():
    answer = answer + InstallJavaHintUbuntu;
    
  return answer;
  
  
def checkJava():  
  try:
    java = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
    return checkJavaVersion(java)
  except OSError:
    return InstallJavaMessage;

def testJavaCheck():
  print "Java: ", checkJava();
   
# ANT
    
def checkAntVersion(ant):
  if "Apache Ant" in ant:
    return True;
  else:
    return "Unrecognized ant version\n"
    
def checkAnt():
  try:
    ant = subprocess.check_output(["ant", "-version"], stderr=subprocess.STDOUT)
    return checkAntVersion(ant)
  except OSError:
    return "No ant installed, please install Apache Ant(TM)\n"

def testAntCheck():
  print "Ant: ", checkAnt();
  
# Preparing a destination directory
    
def prepareDestDir():
  home = os.path.join(expanduser("~"), "mbeddr")
  print("Where would you like to install it["+home+"]: ")
  try:
    destdir = str(raw_input()).strip()
  except EOFError:
    destdir = None
  
  if (destdir is None) or (len(destdir) == 0):
    print("Selecting " + home)
    destdir = home;
    
  try:
    if os.path.exists(destdir):
      print "This directory already exists, please, use another one."
      return False;
    else:
      os.makedirs(destdir)
  except OSError:
    return False;
  
  return destdir;
  
  
  
# Downloading MPS

def MPSFilename():
  url="";
  s = getOs();
  if "Lin" in s:
    url+=MPSLin
  if "Mac" in s:
    url+=MPSMac
  if "Win" in s:
    url+=MPSWin
  return url;

def downloadMPS(dest):
  fName = MPSFilename();
  url = MPSSourceUrl + fName; 
  fName = os.path.join(dest, fName);  
  if os.path.exists(fName):
    return fName;
  else:
    return downloadFile(url, dest);
  



# ------------------ INSTALLING CBMC ------------------

class CBMCInstallerBase:
  
  def getCBMCVersion(self):
    return CBMCVersion + "." + CBMCSubVersion
    
  def checkCBMCVersion(self, cbmc):
    if self.getCBMCVersion() in cbmc:
      return True;
    else:
      return "Unrecognized CBMC C Prover version\n"
       
  def checkCBMC(self):
    try:
      cbmc = subprocess.check_output(["cbmc", "--version"], stderr=subprocess.STDOUT)
      return self.checkCBMCVersion(cbmc)
    except OSError:
      return "No CBMC C Prover installed\n"

  def getCBMCIntro(self):
    return "mbeddr verification heavily relies on CBMC C Prover, which is copyrighted:\n"
   
  def getOnlyCBMCCopyright(self): 
    return """(C) 2001-2008, Daniel Kroening, ETH Zurich,\nEdmund Clarke, Computer Science Department, Carnegie Mellon University\n"""

  def getCBMCCopyright(self): 
    return self.getCBMCIntro() + self.getOnlyCBMCCopyright();
  
  def getCBMCFallbackLicense(self):
    return """(C) 2001-2008, Daniel Kroening, ETH Zurich,
Edmund Clarke, Computer Science Department, Carnegie Mellon University

All rights reserved. Redistribution and use in source and binary forms, with
or without modification, are permitted provided that the following
conditions are met:

  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.

  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

  3. All advertising materials mentioning features or use of this software
     must display the following acknowledgement:

     This product includes software developed by Daniel Kroening,
     ETH Zurich and Edmund Clarke, Computer Science Department,
     Carnegie Mellon University.

  4. Neither the name of the University nor the names of its contributors
     may be used to endorse or promote products derived from this software
     without specific prior written permission.

   
THIS SOFTWARE IS PROVIDED BY THE UNIVERSITIES AND CONTRIBUTORS `AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.\n"""

  def getCBMCLicense(self):
    try:
      return urllib2.urlopen("http://www.cprover.org/cbmc/LICENSE").read();
    except urllib2.HTTPError, e:
      return self.getCBMCFallbackLicense()
    except urllib2.URLError, e:
      return self.getCBMCFallbackLicense()
    except httplib.HTTPException, e:
      return self.getCBMCFallbackLicense()
    except Exception:
      return self.getCBMCFallbackLicense()
    
  
  def installCBMC(self, dest):
    print self.getCBMCLicense();
    print self.getCBMCIntro();
    print "Above is the CBMC license, do you accept it [y/n]?"
    accept = str(raw_input()).strip();
    if "y" != accept:
      return False;
    
    dest = os.path.join(dest, "cbmc");
    if not os.path.exists(dest):
      os.makedirs(dest);
    
    fName = self.downloadCBMC(dest);
    if fName == False:
      return False;
        
    if self.setUpCBMC(dest, fName) != True:
      return False;
    
    c = self.checkCBMC();
    
    if c == True:
      return True;
    else:
      print "Error installing CBMC: " + c;
      return False;    
      
  def downloadCBMC(self, dest):
    print "Not implemented in CBMC Installer Base"
    return False
        
    
class CBMCInstallerForLinux(CBMCInstallerBase):
  def downloadCBMC(self, dest):
    fName = False
    url=""    
    if "Lin32" in getOs():
      url = CBMC32BitLinuxUrl;
    if "Lin64" in getOs():
      url = CBMC64BitLinuxUrl;    
    print "Downloading CBMC: " + url;
    try:
      fName = downloadFile(url, dest);
    except Exception:      
      return False;      
    return fName;
    
  def getCBMCInstallPath(self):  
    return "/usr/bin/cbmc";  
    
  def setUpCBMC(self, dest, fname):
    unarchive(fname, dest);
    print "\nTo finish the CBMC installation, you might be asked for the root/administrator password.\n"
    print "Password: "
    proc = subprocess.Popen(["sudo","-p", "", "ln", "-s", "--force", os.path.join(dest, "cbmc"), self.getCBMCInstallPath()], stdin=subprocess.PIPE)
    proc.wait()
    print "Done\n"
    return True;
    
class CBMCInstallerForMac(CBMCInstallerBase):
  def downloadCBMC(self, dest):
    fName = False
    url = CBMCMacUrl;
    print "Downloading CBMC: " + url;
    try:
      fName = downloadFile(url, dest);
    except Exception:      
      return False;      
    return fName;
    
  def setUpCBMC(self, dest, fname):
    print "\nPlease, proceed installing CBMC..."
    proc = subprocess.Popen(["open", fname], stdin=subprocess.PIPE)
    proc.wait()
    print "Done\n"
    return True;


def getCBMCInstaller():
  if "Lin" in getOs():
    return CBMCInstallerForLinux();
  if "Mac" in getOs():
    return CBMCInstallerForMac();
  return None;

    
    
def testCBMCInstaller():
  dest = prepareDestDir();
  print "Testing CBMC installer";
  installer = getCBMCInstaller();
  installer.installCBMC(dest);
  
print testCBMCInstaller();
exit(0);
     
# ------------------ END INSTALLING CBMC ------------------
    
 
    
def cloneMbeddr(dest, MbeddrDir):
  os.system("git clone " + MbeddrRepo+ " " + MbeddrDir);
  print "Checking out " + TheBranch + " branch..."
  os.system("git --git-dir="+ os.path.join(MbeddrDir, ".git") + " reset --hard");
  os.system("git --git-dir="+ os.path.join(MbeddrDir, ".git") + " checkout " + TheBranch);
    
  
def configureMpsVmopts(MPSDir, MbeddrDir):
    f = open(os.path.join(MPSDir, "bin", "mps.vmoptions"), 'w');
    opts = MPS_VMOPTIONS;
    ConfigPath = os.path.join(MPSDir, "IdeaConfig");
    if not os.path.exists(ConfigPath):
      os.makedirs(ConfigPath);
    opts = opts.replace("IdeaConfig", ConfigPath);
    
    SysPath = os.path.join(MPSDir, "IdeaSystem");
    
    if not os.path.exists(SysPath):
      os.makedirs(SysPath);
    opts = opts.replace("IdeaSystem", SysPath);
    
    f.write(opts);
    f.close();
    
    OptionsPath = os.path.join(ConfigPath, "options");
    if not os.path.exists(OptionsPath):
      os.makedirs(OptionsPath);
    
    f = open(os.path.join(OptionsPath, "libraryManager.xml"), 'w');
    f.write(LIBRARY_MANAGER);
    f. close();
    
    f = open(os.path.join(OptionsPath, "path.macros.xml"), 'w');
    f.write(PATH_MACROS.replace("MbeddrDir", MbeddrDir));
    f. close();
  
def configureMbeddr(MPSDir, MbeddrDir):
  BuildPropsPath = os.path.join(MbeddrDir, "code", "languages", "build.properties");
  f = open(BuildPropsPath, 'w');
  f.write(BUILD_PROPERTIES.replace("MPSDir", MPSDir).replace("MPSCaches", os.path.join(MPSDir, "CachesMbeddr")).replace(
 "MbeddrDir", MbeddrDir));
  f.close();

def buildMbeddr(MbeddrDir):
  BuildPath = os.path.join(MbeddrDir, "code", "languages");
  os.chdir(BuildPath);
  os.system(os.path.join(BuildPath, "buildLanguages.sh"));

def greetings(MPSDir, MbeddrDir):
  print """\nTo start working: Run\n"""+os.path.join(MPSDir, "mps.sh")+"""\nand go through the tutorial project from"""
  print os.path.join(MbeddrDir, "code", "application"),""" folder.\n"""
  
  print """\nVisit mbeddr.com to learn what's new!\n"""
  
  print "\nWelcome to mbeddr. C the difference C the future.\n";
  print "-----------------------------------------------------------\n"
  print """This installer for mbeddr advanced users has been built by molotnikov (at) fortiss (dot) org.\n
Please, let me know, if it does not work for you!"""
  

  
def main():
  print("Welcome!")
  print("You are about to install the last stable version of mbeddr.")

  print "Detecting Git"  
  j = checkGit()
  if j != True:
    print j;
    return 1; 
  
  print "Detecting Java"  
  j = checkJava()
  if j != True:
    print j;
    return 1;  
  
  print "Detecting Ant"
  j = checkAnt()
  if j != True:
    print j;
    return 1;  
  
  print "Preparing destination directory";  
  dest = prepareDestDir();
  if dest == False:
    print "Problem creating destination directory";
    return 1;
  
  MPSDir = os.path.join(dest, "MPS31");
  MbeddrDir = os.path.join(dest, "mbeddr.github");
  
  
  if os.path.exists(MPSDir):
    print "Can not install MPS, the folder " + MPSDir + " already exists, please delete it first or specify a new one."
    exit(1);
  if os.path.exists(MbeddrDir):
    print "Can not install mbeddr, the folder " + MbeddrDir + " already exists, please delete it first or specify a new one.\n"
    print "Don't forget to save your changes if made to mbeddr!"
    exit(1);
    
  
  print "Detecting CBMC"
  installer = getCBMCInstaller();
  if install == None:
    print "Problem configurring CBMC, analyses might not work!"
  else:    
    j = installer.checkCBMC()
    if j != True:
      print j
      if installer.installCBMC(dest) != True:
	print "Failed to install CBMC!\n"
	exit(1);
      else:
	print "CBMC installed!\n"
    else:
      print """You have CBMC already installed."""
      print installer.getCBMCCopyright();
    
  
  
  
  print "Downloading MPS..."
  archive = downloadMPS(dest);      
  print "Extracting..."
  unarchive(archive, dest);  
  print "Deleting archive"
  os.remove(archive);    
  print "Renaming MPS folder"    
  os.rename(os.path.join(dest, MPSArcDir), MPSDir)
  
  print "Cloning mbeddr..."
  cloneMbeddr(dest, MbeddrDir);
  
  print "Setting mps.vmoptions"
  configureMpsVmopts(MPSDir, MbeddrDir);
  
  print "Setting up mbeddr..."
  configureMbeddr(MPSDir, MbeddrDir);

  
  print "Building mbeddr..."
  buildMbeddr(MbeddrDir);
  #Second time, because first time fails shortly after the start,
  print " * Please, notice: BUILD FAILED messages above are known, they do not represent an actual problem.\nBelow this line they should not appear though. It would be an indication of an error."
  buildMbeddr(MbeddrDir);
  
  greetings(MPSDir, MbeddrDir);
  
main();