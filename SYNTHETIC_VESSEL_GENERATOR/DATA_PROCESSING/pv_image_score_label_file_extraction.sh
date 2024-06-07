find /gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_GENERATOR/SYNTHETIC_DATA/UNREALISTIC_BRANCHING_NUM_FOLDERS -type d -name "VRR_*" -exec sh -c '
  for dir do
    pv_file=$(find "$dir" -type f -name "FINAL_PV*")
    score_file=$(find "$dir" -type f -name "FINAL_SCORE*")

    if [ -n "$pv_file" ] && [ -n "$score_file" ]; then
      cp "$pv_file" /gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_GENERATOR/SYNTHETIC_DATA/UNREALISTIC_BRANCHING_NUM/IMAGES/
      cp "$score_file" /gpfs/users/a1836131/FINAL_HPC_SYNTHETIC_VESSEL_GENERATION_CODE/SYNTHETIC_GENERATOR/SYNTHETIC_DATA/UNREALISTIC_BRANCHING_NUM/LABELS/
    fi
  done
' sh {} +