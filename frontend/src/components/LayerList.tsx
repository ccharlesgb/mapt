import React, { FunctionComponent } from "react";
import {
  CollapsibleList,
  ListItem,
  ListItemText,
  SimpleListItem,
} from "@rmwc/list";
import "rmwc/dist/styles";
import autoBind from "react-autobind";
import { Configuration, DefaultApi, DefaultApiFactory } from "../client";
import * as t from "io-ts";
import { isRight } from "fp-ts/Either";

const Layer = t.type({ id: t.number, label: t.string, group: t.string });
const LayerList = t.array(Layer);

interface ILayer {
  id: number;
  label: string;
  active: boolean;
}

type LayerGroupState = {
  layers: ILayer[];
};

type LayerGroupProps = {
  label: string;
  icon: string;
};

export class LayerGroup extends React.Component<
  LayerGroupProps,
  LayerGroupState
> {
  api: ReturnType<typeof DefaultApiFactory>;

  constructor(props: LayerGroupProps) {
    super(props);
    this.state = { layers: [] };
    this.api = new DefaultApi(undefined, "http://localhost:8000");

    autoBind(this);
  }

  componentDidMount() {
    this.api
      .getLayersLayersGet()
      .then((result) => {
        const layers = LayerList.decode(result.data);
        if (isRight(layers)) {
          const newLayers = layers.right.map((value) => {
            return { id: value.id, label: value.label, active: false };
          });
          this.setState({ layers: newLayers });
        } else {
          throw new Error("Bad data!");
        }
      })
      .catch((reason) => {
        console.log(reason);
      });
  }

  render() {
    const listItems = this.state.layers.map((layer) => (
      <LayerListItem key={layer.id} label={layer.label} active={layer.active} />
    ));
    return (
      <CollapsibleList
        handle={
          <SimpleListItem
            text={this.props.label}
            graphic={this.props.icon}
            metaIcon="chevron_right"
          />
        }
      >
        {listItems}
      </CollapsibleList>
    );
  }
}

// export const LayerGroup2: FunctionComponent<LayerGroupProps> = ({label, icon, layers}) => {
//     const listItems = layers.map((layer) => <LayerListItem key={layer.id} label={layer.label}
//                                                            active={layer.active}/>);
//     return (
//         <CollapsibleList
//             handle={<SimpleListItem text={label} graphic={icon} metaIcon="chevron_right"/>}>
//             {listItems}
//         </CollapsibleList>)
// }

type LayerListItemProps = {
  label: string;
  active: boolean;
};

// we can use children even though we haven't defined them in our CardProps
export const LayerListItem: FunctionComponent<LayerListItemProps> = ({
  label,
  active,
}) => (
  <ListItem>
    <ListItemText>{label}</ListItemText>
  </ListItem>
);
