import React from "react";
import { Button } from "@rmwc/button";
import "rmwc/dist/styles";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import MapboxMap from "./MapboxMap";
import UploadModal from "./UploadModal";
import "./Main.css";
import autoBind from "react-autobind";
import {
  CollapsibleList,
  ListDivider,
  SimpleListItem,
  ListOnActionEventT,
  ListItem,
} from "@rmwc/list";

type ModalState = {
  upload: boolean;
};

type ModalStateKeys = keyof ModalState;

type MainState = {
  isOpen: ModalState;
};

type MainProps = {};

class Main extends React.Component<MainProps, MainState> {
  constructor(props: MainProps) {
    super(props);
    this.state = { isOpen: { upload: false } };
    autoBind(this);
  }

  toggleModal(key: ModalStateKeys) {
    console.log(key);
    this.setState({ isOpen: { [key]: !this.state.isOpen[key] } });
  }

  render() {
    return (
      <>
        <Topbar />
        <div className="main-container">
          <div className="sidebar-container">
            <Sidebar
              onUploadClicked={(event: ListOnActionEventT) => {
                this.toggleModal("upload");
              }}
            />
          </div>
          <div className="map-container">
            <MapboxMap />
          </div>
        </div>
        <UploadModal open={this.state.isOpen.upload} />
      </>
    );
  }
}

export default Main;
