#!/bin/bash

read -p "Are you in the root folder of Fridgify? (y/n)" -r choice
case "$choice" in
  y|Y ) echo "Alright. Kicking off process...";;
  n|N ) echo "Please make sure you are in the root folder."; exit 1;;
  * ) echo "Please. Don't do this. Don't try to be funny. Just type in what you're supposed to. Thanks -.-"; exit 1;;
esac

read -p "Did you commit your changes which shall be pushed? (y/n) " -r choice
case "$choice" in
  y|Y ) echo "Alright. Kicking off process...";;
  n|N ) echo "Well, then get back to committing my dude!"; exit 1;;
  * ) echo "Please. Don't do this. Don't try to be funny. Just type in what you're supposed to. Thanks -.-"; exit 1;;
esac

name=$(git config user.name)
email=$(git config user.email)

echo "Pushing commits to currently tracked remote branch..."
git push

echo "Creating temporary directory in parent folder"
mkdir ../tmp

cp tests/features/*.feature ../tmp

echo "Navigating to parent folder of root..."
cd ../tmp || (echo "tmp does not exist"; exit;)

echo "Cloning Fridgify Repository..."
git clone https://github.com/DonkeyCo/Fridgify.git

echo "Move to cloned Fridgify folder..."
cd Fridgify || (echo "Cloned Fridgify folder does not exist"; exit;)

echo "Checkout documentation branch..."
git checkout documentation

if [ ! -d "./documentation/uc/features" ]; then
  echo "No images folder. Creating images folder."
  mkdir ./documentation/uc/features
fi

echo "Copy feature files to destination..."
find .. -type f -name "*.feature" -exec mv {} ./documentation/uc/features \;

for file in ./documentation/uc/features/*.feature
do
  content=$(printf "\`\`\`.feature\n%s\n\`\`\`", "$(cat "$file")")
  filename=$(basename -- "$file")
  mdfn="${filename%.*}".md
  # Something is up with my regex. Replacing works totally fin
  perl -pi.bak -e "s/./a/g" ./documentation/uc/fridgeContent/getContent/getFridgeContentUseCase.md
done

#echo "Set configuration information..."
#git config user.name "$name"
#git config user.email "$email"

#echo "Track changes..."
#git add ./documentation/uc/features

#echo "Commit changes..."
#git commit -m "Feature File System: Automatic Update"

#echo "Push changes..."
#git push

#echo "Remove tmp folder"
#cd ../..
#rm -r -f ./tmp

echo "Process finished."
