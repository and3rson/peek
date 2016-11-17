var addNoteModal = null;

class Header extends React.Component {
    render() {
        return (
            <nav>
                <div className="nav-wrapper red darken-2">
                    <div className="container">
                        <a href="#" className="brand-logo" onClick={() => this.props.page.switchPage('list')}>Peek</a>
                        <ul id="nav-mobile" className="right hide-on-med-and-down">
                            <li><a href="#" onClick={() => $('#add-note-modal').modal('open')}>
                                <i className="material-icons left">add</i>
                                Add
                            </a></li>
                            <li><a href="#" onClick={() => this.props.page.switchPage('settings')}>
                                <i className="material-icons left">settings</i>
                                Settings
                            </a></li>
                        </ul>
                    </div>
                </div>
            </nav>
        );
    }
}

class AddNoteModal extends React.Component {
    render() {
        return (
            <div id="add-note-modal" className="modal">
                <div className="modal-content">
                    <h4>Add Note</h4>
                    <textarea className="materialize-textarea">Some text</textarea>
                </div>
                <div className="modal-footer">
                    <a href="#!" className="modal-action modal-close waves-effect waves-green btn-flat">Save</a>
                </div>
            </div>
        );
    }
}

class NoteItem extends React.Component {
    getContrastingColor(str) {
        var r = parseInt(str.substr(0, 2), 16);
        var g = parseInt(str.substr(2, 2), 16);
        var b = parseInt(str.substr(4, 2), 16);
        var a = 1 - ( 0.299 * r + 0.587 * r + 0.114 * b) / 255;
        if (a < 0.5) {
            // bright colors - black font
            return '#000000';
        } else {
            // dark colors - white font
            return '#FFFFFF';
        }
    }
    render() {
        return (
            <div className="card-panel" style={{
                    backgroundColor: '#' + this.props.data.color,
                    color: this.getContrastingColor(this.props.data.color)
                }}>
                Abc
                {this.props.data.content}
            </div>
        )
    }
}

class List extends React.Component {
    constructor() {
        super();
        this.state = {
            loading: true,
            notes: null
        };
        this.refresh();
    }
    refresh() {
        var self = this;
        fetch('/api/notes', {
            headers: {
                'Authorization': 'Basic ' + btoa('admin:admin')
            }
        }).then(
            (response) => response.json()
        ).then(
            (response) => {
                console.log('Got data:', response);
                self.setState({
                    loading: false,
                    notes: response
                });
            }
        ).catch(
            (error) => {
                console.log('error', error);
            }
        );
    }
    render() {
        if (this.state.loading) {
            return (<div>Loading...</div>);
        } else {
            return (
                <div>
                    <h1>List</h1>
                    <div className="row">
                        {this.state.notes.map((note) => {
                            return (
                                <div className="col s12 m4" key={note.id.toString()}>
                                    <NoteItem data={note} />
                                </div>
                            );
                        })}
                    </div>
                </div>
            )
        }
    }
}

class Page extends React.Component {
    constructor() {
        super();
        this.state = {
            selected: 'list'
        };
    }
    switchPage(page) {
        this.setState({
            selected: page
        });
    }
    render() {
        if (this.state.selected == 'list') {
            return (
                <page>
                    <Header page={this} />
                    <div className="container">
                        <List/>
                    </div>
                </page>
            );
        } else if (this.state.selected == 'settings') {
            return (
                <page>
                    <Header page={this} />
                    <div className="container">
                        <h1>Settings</h1>
                    </div>
                </page>
            );
        }
    }
}

class App extends React.Component {
    render () {
        return (
            <div>
                <Page/>
                <AddNoteModal ref={(el) => { addNoteModal = el }}/>
            </div>
        );
    }
};

$(document).ready(function(){
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
});

ReactDOM.render(
    <App/>,
    document.getElementById('root')
);
