import commands
df = commands.getoutput("df -hP")
#[x.split()[4] for x in df.split("\n")]
print [(x.split()[0], x.split()[4]) for x in df.split("\n") if x.split()[4].endswith("%")]

