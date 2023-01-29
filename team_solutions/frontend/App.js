import React, {Component} from "react";
import {Button, Image, SafeAreaView, StyleSheet, Text, View, Dimensions} from "react-native";

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

let imgDim = 150;
let headerFontSize = 55;

if (windowWidth > 1000) {
    imgDim = 200;
    headerFontSize = 70;
} else {
    imgDim = 100;
    headerFontSize = 40;
}

//Importing the installed libraries
import * as FS from "expo-file-system";
import * as ImagePicker from "expo-image-picker";

export default class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            cameraRollPer: null,
            disableButton: false,
        };
    }

    async componentDidMount() {
        const {status} = await ImagePicker.requestMediaLibraryPermissionsAsync();
        this.setState((state, props) => {
            return {
                cameraRollPer: status === "granted",
                disableButton: false,
            };
        });
    }

    uriToBase64 = async (uri) => {
        return await FS.readAsStringAsync(uri, {
            encoding: FS.EncodingType.Base64,
        });
    };

    pickMedia = async () => {
        this.setState((state, props) => {
            return {
                cameraRollPer: state.cameraRollPer,
                disableButton: true,
            };
        });
        let result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.All,
            base64: true,
        });
        if (result.cancelled) {
            return;
        }
        if (result.type == "image") {
            await this.toServer({
                type: result.type,
                base64: result.base64,
                uri: result.uri,
            });
        } else {
            let base64 = await this.uriToBase64(result.uri);
            await this.toServer({
                type: result.type,
                base64: base64,
                uri: result.uri,
            });
        }
    };

    toServer = async (mediaFile) => {
        let type = mediaFile.type;
        let schema = "http://";
        let host = "10.189.37.233";
        let route = "";
        let port = "5000";
        let url = "";
        let content_type = "";
        type === "image"
            ? ((route = "/image"), (content_type = "image/jpeg"))
            : ((route = "/video"), (content_type = "video/mp4"));
        url = schema + host + ":" + port + route;

        let response = await FS.uploadAsync(url, mediaFile.uri, {
            headers: {
                "content-type": content_type,
            },
            httpMethod: "POST",
            uploadType: FS.FileSystemUploadType.BINARY_CONTENT,
        });

        console.log(response.headers);
        console.log(response.body);
    };

    render() {
        return (
            <SafeAreaView style={styles.container}>
                <View style={styles.headerBox}>
                    <Text style={styles.headerText}>
                        QNN Image Recognition
                    </Text>
                    <Image source={require("./assets/logo.png")}
                           style={{width: imgDim, height: imgDim}}/>
                </View>
                <View style={styles.container}>
                {this.state.cameraRollPer ? (
                    <Button
                        title="Upload an Image"
                        disabled={this.state.disableButton}
                        onPress={async () => {
                            await this.pickMedia();
                            this.setState((s, p) => {
                                return {
                                    cameraRollPer: s.cameraRollPer,
                                    disableButton: false,
                                };
                            });
                        }}
                    />
                ) : (
                    <Text>Camera Roll Permission Required ! </Text>
                )}

                <View style={styles.container}>
                    <Image source={require("./assets/test.jpg")}
                           style={{width: imgDim * 2.5, height: imgDim * 2.5}}/>
                </View>
                </View>
            </SafeAreaView>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#00000",
        alignItems: "center",
        justifyContent:'space-evenly',
    },
    headerText: {
        color: '#ffffff',
        fontSize: headerFontSize,
        fontWeight:'bold',
    },
    headerBox: {
        flex: 0.25,
        flexDirection:'row',
        justifyContent:'space-evenly',
        backgroundColor: 'skyblue',
        width: '100%',
        alignItems: 'center',
    },
});