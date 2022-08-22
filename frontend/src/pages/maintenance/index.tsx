import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {Box, Button, Card, CardActionArea, CardContent, Container, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Fab, FormControl, InputLabel, List, ListItem, MenuItem, Select, SelectChangeEvent, TextField, Typography} from "@mui/material"
import { Add, ArrowBackIos } from "@mui/icons-material";

import { Maintenance } from "../../interfaces/maintenance";
import { MaintenanceElement } from "../../components/maintenance"
import { getMaintenanceById, postService } from "../../services/api";
import { ServiceElement } from "../../components/service";



function MaintenancePage(){
    const {id} = useParams()

    const navigation = useNavigate()
    const [maintenance, setMaintenance] = useState<Maintenance>()
    const [openDialog, setOpenDialog] = useState(false);
    const [newDescription, setNewDescription] = useState<string>("");
    const [newTime, setNewTime] = useState<number>(0);
    const [filterStatus, setFilterStatus] = useState<string>("");
    
    useEffect(() => {
        getMaintenanceById(id)
            .then((response) => {
                setMaintenance(response.data.maintenance)
            })
            .catch((error) => {
                console.log(error)
            })
    }, [])

    const handleClickDialog= () => {
        setOpenDialog(true);
    };
    
    const handleCloseDialog = () => {
        setOpenDialog(false);
    };

    function handleChangeStatus(event: SelectChangeEvent) {
        setFilterStatus(event.target.value as string);
    }

    return (
        <Box>
            <Container
                sx={{
                    padding: '20px',
                }}
            >
                <Box
                    sx={{
                        display: 'flex',
                        flexDirection: 'row',
                    }}
                >
                    <Button
                        onClick={() => navigation(-1)}
                    >
                        <ArrowBackIos sx={{ color: "#000"}}/>
                    </Button>

                    <Typography variant="h1"
                        sx={{
                            fontSize: '2.2rem',
                        }}
                    >
                        Maintenance
                    </Typography>
                </Box>
                <Container
                    sx={{
                        display: 'flex',
                        justifyContent: 'center',
                        margin: '0px',
                        padding: '0px',
                    }}
                >
                    <Card elevation={0}
                        sx={{ 
                            width: '100%',
                            padding: '20px',
                            paddingRight: '0px',
                            minWidth: 345,
                            '& .MuiTouchRipple-root': {display: 'none'},
                          }}
                    >
                        <CardActionArea>
                            <CardContent>
                                {maintenance && (<MaintenanceElement maintenance={maintenance} />)}
                            </CardContent>
                        </CardActionArea>
                    </Card>
                </Container>
                
                <Container>
                    <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                        <InputLabel id="select-status-label">Status</InputLabel>
                        <Select
                            labelId="select-status-label"
                            id="select-status"
                            value={filterStatus}
                            label="Status"
                            onChange={handleChangeStatus}
                        >
                            <MenuItem value="">
                            <em>All</em>
                            </MenuItem>
                            <MenuItem value={"done"}>Done</MenuItem>
                            <MenuItem value={"inProgress"}>In Progress</MenuItem>
                            <MenuItem value={"pending"}>Pending</MenuItem>
                        </Select>
                    </FormControl>
                </Container>

                <List>
                    {maintenance?.services?.filter((service) => {
                            if(filterStatus === "") return true
                            return service.status === filterStatus
                        })
                        .map((service) => (
                        <ListItem key={`service-key-${service.id}`}
                            sx={{
                                display: 'flex',
                                justifyContent: 'center',
                            }}
                        >
                            <Card 
                            sx={{ 
                                width: '100%',
                                minWidth: 345,
                                maxWidth: 445,
                                '& .MuiTouchRipple-root': {display: 'none'},
                            }}
                            >
                            <CardActionArea sx={{
                                paddingTop: '20px',
                            }}>
                                <CardContent>
                                    <ServiceElement service={service} />
                                </CardContent>
                            </CardActionArea>
                            </Card>
                        </ListItem>
                    ))}
                </List>
                
                <Fab aria-label="add" sx={{
                    backgroundColor: '#3f51b5',
                    position: 'absolute',
                    bottom: '20px',
                    right: 'calc(15% - 20px)',
                }}
                onClick={handleClickDialog}
                >
                    <Add sx={{
                        color: '#fff',
                    }}/>
                </Fab>

                <Dialog open={openDialog} onClose={handleCloseDialog}>
                <DialogTitle>Create Service</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                    Please, enter the new service info
                    </DialogContentText>
                    <TextField
                    autoFocus
                    margin="dense"
                    id="description"
                    label="Describe the service"
                    type="text"
                    fullWidth
                    variant="standard"
                    value={newDescription}
                    onChange={(e) => setNewDescription(e.target.value)}
                    />
                    <TextField
                    label="Time in hours"
                    fullWidth
                    type="number"
                    value={newTime}
                    onChange={(e) => {
                        const t = parseInt(e.target.value);
                        setNewTime(t);
                    }}
                    InputLabelProps={{
                        shrink: true,
                    }}
                    variant="standard"
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog}>Cancel</Button>
                    <Button onClick={()=>{
                    if(newDescription !== "" && newTime >= 0){
                        postService({
                            description: newDescription,
                            time: newTime,
                            Maintenance_id: id,
                        })
                        .then(res=>{
                        window.location.reload()
                        })
                        .catch((err)=>{
                        console.log(err)
                        })
                    }
                    handleCloseDialog()
                    }}>Create</Button>
                </DialogActions>
                </Dialog>
            </Container>
        </Box>
    )
}

export default MaintenancePage;