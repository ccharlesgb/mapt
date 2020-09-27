import React from "react";
import { Drawer } from "@rmwc/drawer";
import "rmwc/dist/styles";
import autoBind from "react-autobind";
import "./Sidebar.css";

type SidebarState = {};

type SidebarProps = {};

class Sidebar extends React.Component<SidebarProps, SidebarState> {
  constructor(props: SidebarProps) {
    super(props);
    this.state = {};
    autoBind(this);
  }

  render() {
    return (
      <React.Fragment>
        <Drawer>{this.props.children}</Drawer>
      </React.Fragment>
    );
  }
}

export default Sidebar;
