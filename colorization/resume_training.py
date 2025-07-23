#!/usr/bin/env python3
"""
Kaggle Session Resume Helper for Image Colorization Project
============================================================

This script helps you quickly resume training after a Kaggle session interruption.
It checks for existing checkpoints and provides status information.

Usage:
    python resume_training.py

Features:
- Lists available checkpoints
- Shows training progress
- Estimates completion time
- Provides next steps guidance
"""

import os
import glob
import json
from datetime import datetime
from safetensors.torch import load_file

def check_training_status():
    """Check the current status of training and provide guidance."""
    
    print("🔍 Kaggle Training Session Status Check")
    print("=" * 50)
    
    # Check for checkpoints
    checkpoint_dir = "checkpoints"
    if os.path.exists(checkpoint_dir):
        checkpoint_files = glob.glob(f"{checkpoint_dir}/checkpoint_epoch_*.safetensors")
        
        if checkpoint_files:
            # Get latest checkpoint
            latest_checkpoint = max(checkpoint_files, key=os.path.getctime)
            print(f"✅ Found {len(checkpoint_files)} checkpoint(s)")
            print(f"📍 Latest checkpoint: {os.path.basename(latest_checkpoint)}")
            
            # Load checkpoint info
            try:
                checkpoint_data = load_file(latest_checkpoint)
                epoch = int(checkpoint_data.get('epoch', 0))
                loss = float(checkpoint_data.get('loss', 0))
                timestamp = checkpoint_data.get('timestamp', 'unknown')
                
                print(f"🎯 Last completed epoch: {epoch}")
                print(f"📉 Last loss: {loss:.4f}")
                print(f"⏰ Checkpoint time: {timestamp}")
                
                # Calculate progress
                total_epochs = 50  # From updated configuration
                progress = (epoch + 1) / total_epochs * 100
                remaining_epochs = total_epochs - (epoch + 1)
                
                print(f"📊 Training progress: {progress:.1f}% ({epoch + 1}/{total_epochs} epochs)")
                print(f"🎯 Remaining epochs: {remaining_epochs}")
                
                if remaining_epochs > 0:
                    print(f"\n💡 Next steps:")
                    print(f"   1. Re-run the notebook from the beginning")
                    print(f"   2. Training will automatically resume from epoch {epoch + 1}")
                    print(f"   3. Estimated time: ~{remaining_epochs * 0.2:.1f} hours remaining")
                else:
                    print(f"\n🎉 Training appears to be complete!")
                    
            except Exception as e:
                print(f"⚠️  Could not read checkpoint details: {e}")
                
        else:
            print("⚠️  No checkpoints found in checkpoints/ directory")
            print("💡 Training hasn't started yet or checkpoints were cleared")
    else:
        print("📁 No checkpoints directory found")
        print("💡 Training hasn't been started yet")
    
    # Check for saved models
    if os.path.exists("saved_models"):
        model_files = glob.glob("saved_models/*.safetensors")
        if model_files:
            print(f"\n🎉 Found {len(model_files)} saved model(s)")
            latest_model = max(model_files, key=os.path.getctime)
            print(f"📍 Latest model: {os.path.basename(latest_model)}")
        else:
            print(f"\n📁 saved_models/ directory exists but no models found")
    else:
        print(f"\n📁 No saved_models/ directory found")
    
    # Check dataset
    dataset_path = "/home/loc-dang/.cache/kagglehub/datasets/awsaf49/coco-2017-dataset/versions/2"
    if os.path.exists(dataset_path):
        print(f"\n✅ Dataset found at: {dataset_path}")
    else:
        print(f"\n⚠️  Dataset not found at expected location")
        print(f"💡 You may need to re-download the dataset")
    
    print("\n" + "=" * 50)
    print("🔄 To resume training: Re-run the colorization-model.ipynb notebook")
    print("🚀 The enhanced training loop will automatically continue from where it left off!")

if __name__ == "__main__":
    check_training_status()
