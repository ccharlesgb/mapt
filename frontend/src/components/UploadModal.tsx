import React from "react";

import {Dialog, DialogTitle, DialogContent, DialogButton, DialogActions} from '@rmwc/dialog'
import {FormField} from '@rmwc/formfield'
import 'rmwc/dist/styles'
import autoBind from 'react-autobind';

type UploadModalState = {}

type UploadModalProps = { open: boolean }

class UploadModal extends React.Component<UploadModalProps, UploadModalState> {
    constructor(props: UploadModalProps) {
        super(props)
        this.state = {}
        autoBind(this);
    }

    render() {
        return (
            <Dialog open={this.props.open}>
                <DialogTitle>Upload new Data</DialogTitle>
                <DialogContent>
                    <FormField>
                        <input type="file" id="input"/>
                        <label htmlFor="input">Select file</label>
                    </FormField>
                </DialogContent>
                <DialogActions>
                    <DialogButton action="close">Cancel</DialogButton>
                    <DialogButton action="accept" isDefaultAction>
                        Next
                    </DialogButton>
                </DialogActions>
            </Dialog>
        );
    }
}

export default UploadModal