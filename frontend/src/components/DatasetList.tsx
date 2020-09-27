import React, { FunctionComponent } from "react";
import {
  CollapsibleList,
  ListItem,
  ListItemText,
  SimpleListItem,
  List,
} from "@rmwc/list";
import { CircularProgress } from "@rmwc/circular-progress";
import "rmwc/dist/styles";
import autoBind from "react-autobind";
import { DefaultApi, DefaultApiFactory } from "../client";
import * as t from "io-ts";
import { isRight } from "fp-ts/Either";

const Attribute = t.type({ name: t.string, display: t.string, type: t.string });
const Dataset = t.type({
  id: t.number,
  label: t.string,
  description: t.string,
  schema: t.array(Attribute),
});
const DatasetArray = t.array(Dataset);

interface IAttribute {
  name: string;
  display: string;
  type: string;
}

interface IDataset {
  id: number;
  label: string;
  description: string;
  group: string;
  schema: IAttribute[];
  active: boolean;
}

export type DatasetListFetcherState = {
  isFetching: boolean;
  data: IDataset[];
};

type DatasetListFetcherProps = {
  children(state: DatasetListFetcherState): void;
};

export class DatasetListFetcher extends React.Component<
  DatasetListFetcherProps,
  DatasetListFetcherState
> {
  api: ReturnType<typeof DefaultApiFactory>;

  constructor(props: DatasetListFetcherProps) {
    super(props);
    this.state = { isFetching: true, data: [] };
    this.api = new DefaultApi(undefined, "http://localhost:8000");

    autoBind(this);
  }

  fetchData() {
    this.setState({ isFetching: true });
    this.api
      .getAllDatasetsDatasetsGet()
      .then((result) => {
        const Datasets = DatasetArray.decode(result.data);
        if (isRight(Datasets)) {
          const newDatasets = Datasets.right.map((value) => {
            return {
              id: value.id,
              label: value.label,
              description: value.description,
              active: false,
              schema: [],
              group: "All",
            };
          });
          this.setState({ data: newDatasets });
        } else {
          this.setState({ data: [] });
          throw new Error("Bad data!");
        }
      })
      .catch((reason) => {
        console.log(reason);
      })
      .finally(() => {
        this.setState({ isFetching: false });
      });
  }

  componentDidMount() {
    this.fetchData();
  }

  render() {
    return <>{this.props.children(this.state)}</>;
  }
}

type DatasetListProps = {
  datasetList: DatasetListFetcherState;
};

export const DatasetList: FunctionComponent<DatasetListProps> = (props) => {
  console.log(props.datasetList);
  const isFetching = props.datasetList.isFetching;
  if (isFetching) {
    return (
      <>
        <List>
          <SimpleListItem graphic={<CircularProgress />} text="Loading..." />
        </List>
      </>
    );
  }
  const layersGrouped = new Map();
  props.datasetList.data.forEach((item) => {
    const key = item.group;
    const collection = layersGrouped.get(key);
    if (!collection) {
      layersGrouped.set(key, [item]);
    } else {
      collection.push(item);
    }
  });
  const layerGroups = Array.from(layersGrouped.keys()).map((val) => {
    return (
      <DatasetGroupList
        key={val}
        group_name={val}
        datasets={layersGrouped.get(val)}
      />
    );
  });
  return <List>{layerGroups}</List>;
};

type DatasetGroupListProps = {
  group_name: string;
  datasets: IDataset[];
};

export const DatasetGroupList: FunctionComponent<DatasetGroupListProps> = (
  props
) => {
  const datasetItems = props.datasets.map((val) => {
    return <DatasetListItem dataset={val} />;
  });
  return (
    <>
      <CollapsibleList
        handle={
          <SimpleListItem
            text={props.group_name}
            graphic="subject"
            metaIcon="chevron_right"
          />
        }
      >
        {datasetItems}
      </CollapsibleList>
    </>
  );
};

type DatasetListItemProps = {
  dataset: IDataset;
};

export const DatasetListItem: FunctionComponent<DatasetListItemProps> = (
  props
) => {
  return (
    <>
      <ListItem>
        <ListItemText>{props.dataset.label}</ListItemText>
      </ListItem>
    </>
  );
};
