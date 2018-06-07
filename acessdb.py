from dbclass import dbcon

example = dbcon.query.all()

print(example)

for ex in example:
    print(ex.mobile)

