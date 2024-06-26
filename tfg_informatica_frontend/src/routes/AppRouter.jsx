import {Navigate, Route, Routes } from "react-router-dom"
import { HomePage } from "../pages/HomePage"
import { DevicesPage } from "../pages/DevicesPage"
import { HostsPage } from "../pages/HostsPage"
import DeviceSubPage from "../pages/DeviceSubPage"
import { deviceConfigurationConfig, deviceDataConfig } from "../utils/DeviceViewsConfig"
import { TaskSchedulerPage } from "../pages/TaskSchedulerPage"
import Navbar from "../components/layout/NavBar"
import { TaskEditPage } from "../pages/TaskEditPage"
import { TaskDataPage } from "../pages/TaskDataPage"


export const AppRouter = () => {
  return (
    <>
    <Navbar />
        <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/devices" element={<DevicesPage />} />
            <Route path="/devices/device-data" element={<DeviceSubPage viewsConfig={deviceDataConfig} />} />
            <Route path="/devices/device-configuration" element={<DeviceSubPage viewsConfig={deviceConfigurationConfig} />} />

            <Route path="/task-scheduler" element={<TaskSchedulerPage />}/>
            <Route path="/task-scheduler/task-edit" element={<TaskEditPage />}/>
            <Route path="/task-scheduler/task-data" element={<TaskDataPage/>}/>

            <Route path="/hosts" element={<HostsPage />} />
            
            <Route path="/*" element={<Navigate to="/" />} />
        </Routes>
    </>
);
}
