import sys
print("Python interpreter used by Streamlit:")
print(sys.executable)

print("\nPython search paths:")
for p in sys.path:
    print(" -", p)
