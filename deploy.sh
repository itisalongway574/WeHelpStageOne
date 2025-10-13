#!/bin/bash

# 如果任何指令失敗，就立刻停止執行
set -e

# 檢查是否有提供提交訊息作為參數
if [ -z "$1" ]; then
  echo "錯誤：請提供提交訊息作為第一個參數。"
  echo "用法: ./deploy.sh \"你的提交訊息\""
  exit 1
fi

echo "Step 1: 正在暫存所有變更..."
git add .

echo "Step 2: 正在使用訊息 \"$1\" 提交變更..."
git commit -m "$1"

echo "Step 3: 正在推送到 'main' 分支..."
git push origin main

echo "Step 4: 正在部署到 GitHub Pages ('gh-pages' 分支)..."
git subtree push --prefix=Week.01 origin gh-pages

echo "✅ 部署成功！ main 和 gh-pages 分支都已更新。"
