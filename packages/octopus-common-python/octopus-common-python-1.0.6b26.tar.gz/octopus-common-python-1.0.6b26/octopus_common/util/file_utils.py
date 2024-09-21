def read_properties(file_path):
    properties = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # 跳过空行和注释行
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                properties[key.strip()] = value.strip()
    return properties
