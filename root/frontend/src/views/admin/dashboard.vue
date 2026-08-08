<template>

<h2>Admin Dashboard</h2>

<table>

    <thead>
        <tr>
            <th>Students</th>
            <th>Companies</th>
            <th>Drives</th>
            <th>Applications</th>
        </tr>
    </thead>

    <tbody>
        <tr>
            <td>{{ students }}</td>
            <td>{{ companies }}</td>
            <td>{{ drives }}</td>
            <td>{{ applications }}</td>
        </tr>
    </tbody>

</table>

<br>

<button @click="$router.push('/admin/students')">
    Students
</button>

<button @click="$router.push('/admin/companies')">
    Companies
</button>

<button @click="$router.push('/admin/drives')">
    Drives
</button>

<button @click="$router.push('/admin/applications')">
    Applications
</button>

</template>

<script>

export default{

    data(){

        return{

            students:0,
            companies:0,
            drives:0,
            applications:0

        }

    },

    async mounted(){

        let token=localStorage.getItem("token")

        let response=await fetch("http://127.0.0.1:5000/admin/dashboard",{

            headers:{
                "Authorization":"Bearer "+token
            }

        })

        let data=await response.json()

        this.students=data.students
        this.companies=data.companies
        this.drives=data.drives
        this.applications=data.applications

    }

}

</script>