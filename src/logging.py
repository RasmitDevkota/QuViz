log_label = {
    "ERROR": True,
    "WARNING": True,
    "INFO": True,
}

def log(label, message):
    if label in log_label.keys():
        if not log_label[label]:
            return
    
    print(f"! {label} > {message}")
