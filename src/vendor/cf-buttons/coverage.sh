./node_modules/react-tools/bin/jsx -x jsx ./src/ ./coverage/dist
./node_modules/istanbul/lib/cli.js cover -x spec/**/* ./node_modules/jasmine-node/bin/jasmine-node ./spec/
