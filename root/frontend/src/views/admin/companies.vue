<template>

<h2>Companies</h2>

<input type="text" placeholder="Search" v-model="search" @input="getCompanies">

<br><br>

<table border="1">

    <thead>
        <tr>
            <th>ID</th>
            <th>Company</th>
            <th>Email</th>
            <th>Industry</th>
            <th>Location</th>
            <th>HR Contact</th>
            <th>Website</th>
            <th>Approval</th>
            <th>Blacklist Status</th>
            <th>Actions</th>
            <th>Blacklist</th>
        </tr>
    </thead>

    <tbody>

        <tr v-for="company in companies" :key="company.cid">

            <td>{{ company.cid }}</td>
            <td>{{ company.company_name }}</td>
            <td>{{ company.email }}</td>
            <td>{{ company.industry }}</td>
            <td>{{ company.location }}</td>
            <td>{{ company.hr_contact }}</td>
            <td>{{ company.website }}</td>
            <td>{{ company.approval_status }}</td>
            <td>{{ company.blacklisted ? "Blocked" : "Not Blocked" }}</td>

            <td>
                <button @click="$router.push('/admin/company/' + company.cid + '/drives')">View Drives</button>

                <button v-if="company.approval_status == 'Pending'" @click="approve(company.cid)">Approve</button>

                <button v-if="company.approval_status == 'Pending'" @click="reject(company.cid)">Reject</button>
            </td>

            <td>
                <button v-if="!company.blacklisted" @click="blacklist(company.cid)">Blacklist</button>

                <button v-else @click="unblacklist(company.cid)">Unblacklist</button>
            </td>

        </tr>

    </tbody>

</table>

</template>

<script>

export default{

    data(){

        return{
            companies:[],
            search:""
        }

    },

    methods:{

        async getCompanies(){

            let response=await fetch(
                "http://127.0.0.1:5000/admin/companies?search="+this.search,
                {
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    }
                }
            )

            this.companies=await response.json()

        },

        async approve(cid){

            await fetch(
                "http://127.0.0.1:5000/admin/company/"+cid+"/approve",
                {
                    method:"PUT",
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    }
                }
            )

            this.getCompanies()

        },

        async reject(cid){

            await fetch(
                "http://127.0.0.1:5000/admin/company/"+cid+"/reject",
                {
                    method:"PUT",
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    }
                }
            )

            this.getCompanies()

        },

        async blacklist(cid){

            await fetch(
                "http://127.0.0.1:5000/admin/company/"+cid+"/blacklist",
                {
                    method:"PUT",
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    }
                }
            )

            this.getCompanies()

        },

        async unblacklist(cid){

            await fetch(
                "http://127.0.0.1:5000/admin/company/"+cid+"/unblacklist",
                {
                    method:"PUT",
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    }
                }
            )

            this.getCompanies()

        }

    },

    mounted(){

        this.getCompanies()

    }

}

</script>