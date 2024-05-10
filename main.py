
from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import subprocess

app = FastAPI()

@app.post("/predict-bmi/")
async def predict_bmi_from_image(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = os.path.join("temp_images", file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    try:
        # Run the Code2.py script
        command = f"python3 Code2.py"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        if error:
            raise HTTPException(status_code=500, detail=error.decode())

        # Extract BMI value from the output
        output_lines = output.decode().split("\n")
        bmi_value = None
        for line in output_lines:
            if "BMI:" in line:
                bmi_value = float(line.split("BMI:")[1].strip())
                break
        
        # Classify BMI
        bmi_category = None
        if bmi_value is not None:
            if bmi_value < 18.5:
                bmi_category = "Underweight"
            elif 18.5 <= bmi_value < 24.9:
                bmi_category = "Normal"
            elif 25.0 <= bmi_value < 29.9:
                bmi_category = "Overweight"
            elif bmi_value >= 30.0:
                bmi_category = "Obese"

        return {"BMI": bmi_value, "Category": bmi_category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Remove the uploaded image file
        os.remove(file_path)
