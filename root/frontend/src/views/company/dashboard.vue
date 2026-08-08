<template>

<h2>{{ company.company_name }} Dashboard</h2>

<button @click="$router.push('/company/profile')">Update Profile</button>

<table border="1">

    <thead>
        <tr>
            <th>Total Drives</th>
            <th>Total Applications</th>
            <th>Selected Students</th>
        </tr>
    </thead>

    <tbody>
        <tr>
            <td>{{ summary.total_drives }}</td>
            <td>{{ summary.total_applications }}</td>
            <td>{{ summary.selected_students }}</td>
        </tr>
    </tbody>

</table>

<br>

<input type="text" placeholder="Search drives" v-model="search" @input="getDashboard">

<button @click="clearSearch">Clear</button>

<br><br>

<table border="1">

    <thead>
        <tr>
            <th>ID</th>
            <th>Job Title</th>
            <th>Course</th>
            <th>Salary</th>
            <th>Deadline</th>
            <th>Approval</th>
            <th>Status</th>
            <th>Applications</th>
            <th>Action</th>
        </tr>
    </thead>

    <tbody>

        <tr v-if="drives.length == 0">
            <td colspan="9">No drives found</td>
        </tr>

        <tr v-else v-for="drive in drives" :key="drive.did">

            <td>{{ drive.did }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.course }}</td>
            <td>{{ drive.salary }}</td>
            <td>{{ drive.application_deadline }}</td>
            <td>{{ drive.approval_status }}</td>
            <td>{{ drive.status }}</td>
            <td>{{ drive.applications }}</td>

            <td>
                <button @click="$router.push('/company/drive/' + drive.did + '/edit')">Edit</button>
                <button @click="$router.push('/company/drive/' + drive.did + '/applications')">View Applications</button>
            </td>

        </tr>

    </tbody>

</table>

<br>

<button @click="$router.push('/company/drive/create')">Create Drive</button>

<button @click="logout">Logout</button>

</template>


<script>

export default{

    data(){

        return{
            company:{},
            summary:{
                total_drives:0,
                total_applications:0,
                selected_students:0
            },
            drives:[],
            search:""
        }

    },

    methods:{

        async getDashboard(){

            let response=await fetch(
                "http://127.0.0.1:5000/company/dashboard?search="+this.search,
                {
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    },

                    credentials: "include"
                }
            )

            let data=await response.json()

            this.company=data.company
            this.summary=data.summary
            this.drives=data.drives

        },

        clearSearch(){

            this.search=""
            this.getDashboard()

        },

        logout(){

            localStorage.removeItem("token")
            this.$router.push("/")

        }

    },

    mounted(){

        this.getDashboard()

    }

}

</script>