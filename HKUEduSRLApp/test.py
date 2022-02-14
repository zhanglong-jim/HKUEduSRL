a = '{"meta":{"author":"ZhangLong"},"format":"node_tree","data":{"id":"root","topic":"mysrl_name","expanded":true}}'
name = re.findall(r"{\"id\":\"root\",\"topic\":\"(.+?)\"",a)
print(name)