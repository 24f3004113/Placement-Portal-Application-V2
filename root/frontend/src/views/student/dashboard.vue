<template>

    <h2>Student Dashboard</h2>

    <p>Welcome {{ student }}</p>

    <button @click="$router.push('/student/profile/update')">View/Update Profile</button>

    <button @click="$router.push('/student/resume/update')">VIew/Update Resume</button>

    <table border="1">
        <thead>
            <tr>
                <th>Total Applications</th>
                <th>Shortlisted</th>
                <th>Interviews</th>
                <th>Placements</th>
            </tr>
        </thead>

        <tbody>
            <tr>
                <td>{{ total_applications }}</td>
                <td>{{ shortlisted }}</td>
                <td>{{ interviews }}</td>
                <td>{{ placements }}</td>
            </tr>
        </tbody>
    </table>

    <br>

    <h3>Available Placement Drives</h3>

    <input type="text" placeholder="Search Company, Job or Description" v-model="search" @input="getDashboard">

    <button @click="clearSearch">Clear</button>

    <br><br>

    <table border="1">

        <thead>
            <tr>
                <th>ID</th>
                <th>Company</th>
                <th>Job Title</th>
                <th>Salary</th>
                <th>Application Deadline</th>
                <th>Actions</th>
            </tr>
        </thead>

        <tbody>

            <tr v-if="drives.length == 0">
                <td colspan="6">No placement drives found</td>
            </tr>

            <tr v-else v-for="drive in drives" :key="drive.did">

                <td>{{ drive.did }}</td>
                <td>{{ drive.company }}</td>
                <td>{{ drive.job_title }}</td>
                <td>{{ drive.salary }}</td>
                <td>{{ drive.application_deadline }}</td>

                <td>
                    <button @click="$router.push('/student/drive/' + drive.did)">View Details</button>
                    <button v-if="!drive.applied" @click="apply(drive.did)">Apply</button>
                    <button v-else disabled>Already Applied</button>
                </td>

            </tr>

        </tbody>

    </table>

    <br>

    <button @click="logout">Logout</button>

</template>

<script>

export default {

    data() {
        return {
            student: "",
            total_applications: 0,
            shortlisted: 0,
            interviews: 0,
            placements: 0,
            drives: [],
            search: ""
        }
    },

    methods: {

        async getDashboard() {

            let response = await fetch(
                "http://127.0.0.1:5000/student/dashboard?search=" + this.search,
                {
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            this.student = data.student
            this.total_applications = data.total_applications
            this.shortlisted = data.shortlisted
            this.interviews = data.interviews
            this.placements = data.placements
            this.drives = data.available_drives
        },

        clearSearch() {
            this.search = ""
            this.getDashboard()
        },

        async apply(did) {

            let response = await fetch(
                "http://127.0.0.1:5000/student/drive/" + did + "/apply",
                {
                    method: "POST",
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            alert(data.message)

            if (response.ok)
                this.getDashboard()
        },

        logout() {
            localStorage.removeItem("token")
            this.$router.push("/")
        }

    },

    mounted() {
        this.getDashboard()
    }

}

</script>